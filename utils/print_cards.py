# utils/print_cards.py
# Landscape voting cards with sponsor-tier layout and scan-safe QR rendering

from __future__ import annotations

import io
import os
from typing import Any, List, Optional, Tuple

import qrcode
from PIL import Image

CATEGORY_SLUGS: List[Tuple[str, str]] = [
    ("army", "Army"),
    ("navy", "Navy"),
    ("marines", "Marines"),
    ("air-force", "Air Force"),
    ("peoples-choice", "People’s Choice"),
]

VOTE_QR_BOX_SIZE = 8
VOTE_QR_BORDER = 4
REGISTER_QR_BOX_SIZE = 10
REGISTER_QR_BORDER = 4


def safe_open_rgba(path: str) -> Optional[Image.Image]:
    try:
        if not path:
            return None
        return Image.open(path).convert("RGBA")
    except Exception:
        return None


def make_qr(url: str, box_size: int = 8, border: int = 4) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def draw_image_contain(c: Any, img: Image.Image, x: float, y: float, w: float, h: float) -> None:
    from reportlab.lib.utils import ImageReader

    iw, ih = img.size
    if iw <= 0 or ih <= 0:
        return

    scale = min(w / iw, h / ih)
    nw, nh = iw * scale, ih * scale
    dx, dy = x + (w - nw) / 2, y + (h - nh) / 2

    rgba = img if img.mode == "RGBA" else img.convert("RGBA")
    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    bg.alpha_composite(rgba)
    final = bg.convert("RGB")

    c.drawImage(ImageReader(final), dx, dy, width=nw, height=nh, mask="auto")


def _norm_tier(s: dict) -> str:
    raw = (s.get("tier") or s.get("placement") or "standard").strip().lower()
    if raw in {"presenting", "title", "gold", "silver", "standard"}:
        return raw
    return "standard"


def _dedupe_sponsors(rows: List[dict]) -> List[dict]:
    seen = set()
    out: List[dict] = []
    for s in rows:
        key = (
            s.get("id"),
            (s.get("name") or "").strip().lower(),
            (s.get("logo_path") or "").strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def build_landscape_cards_pdf(
    *,
    show: dict,
    cars_rows: List[dict],
    base_url: str,
    static_root: str,
    title_sponsor: Optional[dict],
    sponsors: List[dict],
    judging_classes: Optional[List[dict]] = None,
    include_back: bool = False,
    mirror_back_pages: bool = False,
) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas as rl_canvas

    page_w, page_h = landscape(letter)
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=landscape(letter))

    def static_fs(rel_path: str) -> str:
        return os.path.join(static_root, rel_path.replace("/", os.sep))

    def sponsor_logo_img(s: Optional[dict]) -> Optional[Image.Image]:
        if not s:
            return None
        lp = (s.get("logo_path") or "").strip()
        if not lp:
            return None
        return safe_open_rgba(static_fs(lp))

    def draw_box(
        x: float,
        y: float,
        w: float,
        h: float,
        stroke=colors.black,
        fill=None,
        lw: float = 1.0,
    ) -> None:
        c.saveState()
        c.setLineWidth(lw)
        c.setStrokeColor(stroke)
        if fill is not None:
            c.setFillColor(fill)
            c.rect(x, y, w, h, stroke=1, fill=1)
        else:
            c.rect(x, y, w, h, stroke=1, fill=0)
        c.restoreState()

    def draw_logo_row(
        logo_imgs: List[Image.Image],
        x: float,
        y: float,
        w: float,
        h: float,
        max_items: int,
    ) -> None:
        if not logo_imgs:
            return

        items = logo_imgs[:max_items]
        if not items:
            return

        gap = 8
        count = len(items)
        cell_w = (w - gap * (count - 1)) / count if count else w

        for i, img in enumerate(items):
            draw_image_contain(c, img, x + i * (cell_w + gap), y, cell_w, h)

    def show_text(key: str, default: str = "") -> str:
        try:
            value = show.get(key, default)
        except Exception:
            value = default
        return str(value or default or "").strip()

    def show_int(key: str, default: int = 0) -> int:
        try:
            return int(show.get(key, default) or default)
        except Exception:
            return default

    def card_layout_mode() -> str:
        mode = show_text("card_layout_mode", "auto").lower()
        return mode if mode in {"auto", "voting", "information", "sponsor"} else "auto"

    def voting_enabled_by_show() -> bool:
        if show_int("voting_open", 0) != 1:
            return False
        if show_text("voting_mode", "fundraiser_unlimited").lower() == "none":
            return False
        if show_text("payment_mode", "stripe").lower() == "none":
            return False
        if show_text("show_type", "full").lower() == "cruise_in":
            return False
        return True

    def card_is_voting() -> bool:
        mode = card_layout_mode()
        if mode == "voting":
            return True
        if mode in {"information", "sponsor"}:
            return False
        return voting_enabled_by_show()

    def participant_restricted_voting() -> bool:
        return show_text("voting_mode", "fundraiser_unlimited").lower() == "participant_restricted"

    def car_is_placeholder(row: dict) -> bool:
        try:
            return int(row.get("is_placeholder") or 0) == 1
        except Exception:
            return False

    def info_url() -> str:
        return (
            show_text("cta_url")
            or show_text("external_payment_url")
            or f"{base_url.rstrip('/')}/show/{show_text('slug')}"
        )

    def wrap_text(text: str, max_chars: int) -> List[str]:
        words = str(text or "").replace("\r", "").split()
        lines: List[str] = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    brand_logo = safe_open_rgba(static_fs("img/karmankarshows-logo.png"))

    sponsor_rows: List[dict] = []
    if title_sponsor:
        sponsor_rows.append(dict(title_sponsor))
    sponsor_rows.extend([dict(s) for s in (sponsors or [])])
    sponsor_rows = _dedupe_sponsors(sponsor_rows)

    sponsor_with_imgs: List[Tuple[dict, Image.Image]] = []
    for s in sponsor_rows:
        img = sponsor_logo_img(s)
        if img:
            sponsor_with_imgs.append((s, img))

    presenting_imgs: List[Image.Image] = []
    title_imgs: List[Image.Image] = []
    gold_imgs: List[Image.Image] = []
    silver_imgs: List[Image.Image] = []
    standard_imgs: List[Image.Image] = []

    for s, img in sponsor_with_imgs:
        tier = _norm_tier(s)
        if tier == "presenting":
            presenting_imgs.append(img)
        elif tier == "title":
            title_imgs.append(img)
        elif tier == "gold":
            gold_imgs.append(img)
        elif tier == "silver":
            silver_imgs.append(img)
        else:
            standard_imgs.append(img)

    if not presenting_imgs:
        if title_sponsor:
            fallback_img = sponsor_logo_img(dict(title_sponsor))
            if fallback_img:
                presenting_imgs = [fallback_img]

        if not presenting_imgs and sponsor_with_imgs:
            presenting_imgs = [sponsor_with_imgs[0][1]]

    margin = 0.50 * inch

    for r in cars_rows:
        car_number = int(r["car_number"])
        car_token = str(r["car_token"])
        owner_name = (r.get("owner_name") or "").strip() or "_________________________"
        year = (r.get("year") or "").strip()
        make = (r.get("make") or "").strip()
        model = (r.get("model") or "").strip()

        vehicle_parts = [p for p in [year, make, model] if p and p.upper() != "TBD"]
        vehicle_text = " ".join(vehicle_parts) if vehicle_parts else "_________________________________________"
        class_name = (r.get("judging_class_name") or "").strip()
        class_code = (r.get("judging_class_code") or "").strip()
        class_needs_review = int(r.get("class_needs_review") or 0) == 1
        if class_name:
            class_text = f"{class_code} - {class_name}" if class_code else class_name
        elif class_needs_review:
            class_text = "STAFF REVIEW"
        else:
            class_text = "____________________________"

        is_voting_card = card_is_voting()
        mode = card_layout_mode()
        default_headline = "SCAN TO VOTE" if is_voting_card else ("SPONSOR INFO" if mode == "sponsor" else "EVENT INFO")
        card_headline = show_text("card_headline") or default_headline
        card_subheadline = show_text("card_subheadline") or show_text("title")
        card_message = show_text("qr_message") or (
            "Scan the code for event details, schedule, location information, and updates."
            if not is_voting_card
            else "Scan a category code to vote for this vehicle. Votes are counted according to this show's voting rules."
        )
        info_qr_label = show_text("cta_label") or "More information"
        info_qr_url = info_url()

        # FRONT
        c.setTitle(f"{show.get('title', 'Voting Cards')} - Car #{car_number}")

        header_h = 1.45 * inch
        header_y = page_h - margin - header_h
        draw_box(margin, header_y, page_w - 2 * margin, header_h, lw=1.2)

        if brand_logo:
            draw_image_contain(
                c,
                brand_logo,
                margin + 6,
                header_y + 6,
                1.65 * inch,
                header_h - 12,
            )

        if presenting_imgs:
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(page_w / 2, page_h - margin - 12, "PRESENTED BY")
            draw_image_contain(
                c,
                presenting_imgs[0],
                (page_w / 2) - 1.95 * inch,
                header_y + 0.36 * inch,
                3.90 * inch,
                0.72 * inch,
            )

        c.setFont("Helvetica-Bold", 24)
        c.drawRightString(page_w - margin - 10, header_y + 0.78 * inch, f"CAR #{car_number}")
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(page_w - margin - 10, header_y + 0.53 * inch, card_headline[:34])
        c.setFont("Helvetica", 10)
        c.drawRightString(page_w - margin - 10, header_y + 0.34 * inch, card_subheadline[:60])

        body_y = margin + 1.25 * inch
        body_h = 4.85 * inch
        total_w = page_w - 2 * margin
        left_w = 2.45 * inch
        gap = 0.16 * inch
        right_w = total_w - left_w - gap

        draw_box(margin, body_y, left_w, body_h, lw=1.0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin + 10, body_y + body_h - 22, "VEHICLE INFO")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 10, body_y + body_h - 48, "Owner")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 10, body_y + body_h - 64, owner_name[:32])

        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 10, body_y + body_h - 94, "Vehicle")
        c.setFont("Helvetica", 11)
        c.drawString(margin + 10, body_y + body_h - 110, vehicle_text[:40])

        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 10, body_y + body_h - 132, "Class")
        c.setFont("Helvetica", 10)
        c.drawString(margin + 10, body_y + body_h - 148, class_text[:42])

        if is_voting_card:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin + 10, body_y + body_h - 174, "How voting works")
            c.setFont("Helvetica", 10)
            info_lines = [
                "1. Scan a code on the right.",
                "2. Choose the number of votes.",
                "3. Complete payment if required.",
                "Votes are counted according",
                "to this show's rules.",
            ]
            yy = body_y + body_h - 190
            for line in info_lines:
                c.drawString(margin + 12, yy, line)
                yy -= 14

            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin + 10, body_y + 92, "Award notes")

            c.setFont("Helvetica", 8.5)
            branch_lines = [
                "Scan the category that matches",
                "your vote. Event staff may",
                "adjust categories per show.",
            ]
            yy = body_y + 76
            for line in branch_lines:
                c.drawString(margin + 12, yy, line)
                yy -= 10
        else:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin + 10, body_y + body_h - 174, "Event information")
            c.setFont("Helvetica", 9.5)
            yy = body_y + body_h - 192
            for line in wrap_text(card_message, 32)[:10]:
                c.drawString(margin + 12, yy, line)
                yy -= 13

            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin + 10, body_y + 56, info_qr_label[:30])
            c.setFont("Helvetica", 8.5)
            c.drawString(margin + 12, body_y + 42, "Scan the large code for details.")

        qr_x = margin + left_w + gap
        qr_y = body_y
        qr_h = body_h
        draw_box(qr_x, qr_y, right_w, qr_h, lw=1.0)

        if is_voting_card:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(qr_x + 10, qr_y + qr_h - 20, "Vote for this vehicle")

            cols = 4
            rows = 2
            inner_pad_x = 10
            inner_pad_y = 14
            top_reserved = 24

            cell_w = (right_w - (inner_pad_x * 2)) / cols
            cell_h = (qr_h - top_reserved - (inner_pad_y * 2)) / rows

            grid_items: List[Tuple[str, str]] = CATEGORY_SLUGS + [("", "INFO")]

            for i in range(len(grid_items)):
                col = i % cols
                row = i // cols
                x0 = qr_x + inner_pad_x + col * cell_w
                y0 = qr_y + qr_h - top_reserved - inner_pad_y - (row + 1) * cell_h

                slug, label = grid_items[i]

                if slug:
                    vote_url = f"{base_url.rstrip('/')}/v/{show['slug']}/{car_token}/{slug}"
                    qr_img = make_qr(vote_url, box_size=VOTE_QR_BOX_SIZE, border=VOTE_QR_BORDER)

                    qr_box = min(cell_w - 16, cell_h - 30)
                    qr_draw_x = x0 + (cell_w - qr_box) / 2
                    qr_draw_y = y0 + 22

                    c.saveState()
                    c.setFillColor(colors.white)
                    c.rect(qr_draw_x - 4, qr_draw_y - 4, qr_box + 8, qr_box + 8, stroke=0, fill=1)
                    c.restoreState()

                    draw_image_contain(c, qr_img, qr_draw_x, qr_draw_y, qr_box, qr_box)

                    c.setFont("Helvetica", 9)
                    c.drawCentredString(x0 + cell_w / 2, y0 + 8, label)

                else:
                    c.saveState()
                    c.setFillColor(colors.whitesmoke)
                    c.rect(x0 + 8, y0 + 10, cell_w - 16, cell_h - 20, stroke=0, fill=1)
                    c.restoreState()

                    c.setFont("Helvetica-Bold", 10)
                    c.drawCentredString(x0 + cell_w / 2, y0 + cell_h - 32, "Scan any")
                    c.drawCentredString(x0 + cell_w / 2, y0 + cell_h - 46, "code")
                    c.setFont("Helvetica", 10)
                    c.drawCentredString(x0 + cell_w / 2, y0 + cell_h - 74, "Vote for")
                    c.drawCentredString(x0 + cell_w / 2, y0 + cell_h - 88, "this")
                    c.drawCentredString(x0 + cell_w / 2, y0 + cell_h - 102, "vehicle")
        else:
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(qr_x + right_w / 2, qr_y + qr_h - 34, card_headline[:40])
            c.setFont("Helvetica", 11)
            c.drawCentredString(qr_x + right_w / 2, qr_y + qr_h - 54, card_subheadline[:70])

            qr_img = make_qr(info_qr_url, box_size=REGISTER_QR_BOX_SIZE, border=REGISTER_QR_BORDER)
            qr_box = min(2.55 * inch, qr_h - 1.45 * inch, right_w * 0.48)
            qr_draw_x = qr_x + 0.32 * inch
            qr_draw_y = qr_y + 0.78 * inch

            c.saveState()
            c.setFillColor(colors.white)
            c.rect(qr_draw_x - 8, qr_draw_y - 8, qr_box + 16, qr_box + 16, stroke=0, fill=1)
            c.restoreState()
            draw_image_contain(c, qr_img, qr_draw_x, qr_draw_y, qr_box, qr_box)

            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(qr_draw_x + qr_box / 2, qr_draw_y - 18, info_qr_label[:34])

            text_x = qr_draw_x + qr_box + 0.35 * inch
            text_top = qr_y + qr_h - 86
            c.setFont("Helvetica-Bold", 14)
            c.drawString(text_x, text_top, "Event details")
            c.setFont("Helvetica", 11)
            yy = text_top - 22
            for line in wrap_text(card_message, 44)[:8]:
                c.drawString(text_x, yy, line)
                yy -= 16

            if show_text("location_name"):
                yy -= 8
                c.setFont("Helvetica-Bold", 11)
                c.drawString(text_x, yy, "Location")
                yy -= 15
                c.setFont("Helvetica", 10)
                c.drawString(text_x, yy, show_text("location_name")[:48])

            if show_text("date") or show_text("show_start_time") or show_text("show_end_time"):
                yy -= 22
                c.setFont("Helvetica-Bold", 11)
                c.drawString(text_x, yy, "When")
                yy -= 15
                c.setFont("Helvetica", 10)
                when_line = " ".join([p for p in [show_text("date"), show_text("show_start_time"), show_text("show_end_time")] if p])
                c.drawString(text_x, yy, when_line[:58])

        sponsor_band_h = 1.20 * inch
        sponsor_band_y = margin
        draw_box(margin, sponsor_band_y, page_w - 2 * margin, sponsor_band_h, lw=1.0)

        left_band_w = (page_w - 2 * margin - 8) / 2
        right_band_w = left_band_w

        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(
            margin + left_band_w / 2,
            sponsor_band_y + sponsor_band_h - 14,
            "TITLE SPONSORS",
        )
        if title_imgs:
            draw_logo_row(
                title_imgs,
                margin + 10,
                sponsor_band_y + 0.28 * inch,
                left_band_w - 20,
                0.42 * inch,
                max_items=2,
            )

        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(
            margin + left_band_w + 8 + right_band_w / 2,
            sponsor_band_y + sponsor_band_h - 14,
            "GOLD SPONSORS",
        )
        if gold_imgs:
            draw_logo_row(
                gold_imgs,
                margin + left_band_w + 18,
                sponsor_band_y + 0.24 * inch,
                right_band_w - 20,
                0.46 * inch,
                max_items=4,
            )

        c.showPage()

        # BACK
        if include_back:
            if mirror_back_pages:
                c.saveState()
                c.translate(page_w, 0)
                c.scale(-1, 1)

            back_header_h = 1.20 * inch
            back_header_y = page_h - margin - back_header_h
            draw_box(margin, back_header_y, page_w - 2 * margin, back_header_h, lw=1.2)

            if presenting_imgs:
                c.setFont("Helvetica-Bold", 10)
                c.drawCentredString(page_w / 2, page_h - margin - 10, "PRESENTED BY")
                draw_image_contain(
                    c,
                    presenting_imgs[0],
                    (page_w / 2) - 1.85 * inch,
                    back_header_y + 0.14 * inch,
                    3.70 * inch,
                    0.50 * inch,
                )

            back_is_vote_access = participant_restricted_voting() and not car_is_placeholder(dict(car))
            back_title = "VOTING ACCESS" if back_is_vote_access else "REGISTER THIS CAR"
            back_subtitle = f"Activate voting access for car #{car_number}" if back_is_vote_access else f"Claim car #{car_number} and complete registration"

            c.setFont("Helvetica-Bold", 24)
            c.drawRightString(page_w - margin - 10, back_header_y + 0.58 * inch, back_title)
            c.setFont("Helvetica", 11)
            c.drawRightString(
                page_w - margin - 10,
                back_header_y + 0.30 * inch,
                back_subtitle,
            )

            claim_url = f"{base_url.rstrip('/')}/vote-access/{show['slug']}/{car_token}" if back_is_vote_access else f"{base_url.rstrip('/')}/claim/{show['slug']}/{car_token}"
            qr_back = make_qr(claim_url, box_size=REGISTER_QR_BOX_SIZE, border=REGISTER_QR_BORDER)

            qr_box_size = 2.60 * inch
            qx = margin + 0.40 * inch
            qy = page_h - margin - back_header_h - qr_box_size - 0.40 * inch
            draw_box(qx - 8, qy - 8, qr_box_size + 16, qr_box_size + 34, lw=1.0)

            c.saveState()
            c.setFillColor(colors.white)
            c.rect(qx - 4, qy - 4, qr_box_size + 8, qr_box_size + 8, stroke=0, fill=1)
            c.restoreState()

            draw_image_contain(c, qr_back, qx, qy, qr_box_size, qr_box_size)

            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(qx + qr_box_size / 2, qy - 4, "SCAN FOR VOTING ACCESS" if back_is_vote_access else "SCAN TO REGISTER THIS CAR")

            steps_x = qx + qr_box_size + 0.45 * inch
            steps_y = qy + qr_box_size - 2
            steps_w = page_w - margin - steps_x
            draw_box(steps_x, qy - 8, steps_w, qr_box_size + 16, lw=1.0)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(steps_x + 12, steps_y, "Quick steps")

            c.setFont("Helvetica", 12)
            if back_is_vote_access:
                step_lines = [
                    "1. Scan the QR code to activate voting access.",
                    "2. Scan vehicle voting QR codes on the front of cards.",
                    "3. Vote once per category.",
                    "4. You may change votes until voting closes.",
                ]
            else:
                step_lines = [
                    "1. Scan the QR code.",
                    "2. Enter owner and vehicle information.",
                    "3. Sign the waiver electronically.",
                    "4. Payment was already collected at the booth.",
                ]
            yy = steps_y - 26
            for line in step_lines:
                c.drawString(steps_x + 16, yy, line)
                yy -= 24

            c.setFont("Helvetica-Bold", 11)
            c.drawString(
                steps_x + 12,
                yy - 4,
                "This event is made possible by the generous support of:",
            )

            sponsors_y = margin + 0.08 * inch
            sponsors_h = 1.55 * inch
            draw_box(margin, sponsors_y, page_w - 2 * margin, sponsors_h, lw=1.0)

            c.saveState()
            c.setFillColor(colors.HexColor("#1f4e79"))
            c.rect(
                margin,
                sponsors_y + sponsors_h - 0.34 * inch,
                page_w - 2 * margin,
                0.34 * inch,
                stroke=0,
                fill=1,
            )
            c.restoreState()

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(
                page_w / 2,
                sponsors_y + sponsors_h - 0.23 * inch,
                "THANK YOU TO OUR EVENT SPONSORS",
            )
            c.setFillColor(colors.black)

            if silver_imgs:
                draw_logo_row(
                    silver_imgs,
                    margin + 10,
                    sponsors_y + 0.72 * inch,
                    page_w - 2 * margin - 20,
                    0.28 * inch,
                    max_items=6,
                )

            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin + 10, sponsors_y + 0.44 * inch, "COMMUNITY / SUPPORTING SPONSORS")
            if standard_imgs:
                draw_logo_row(
                    standard_imgs,
                    margin + 10,
                    sponsors_y + 0.08 * inch,
                    page_w - 2 * margin - 20,
                    0.22 * inch,
                    max_items=8,
                )

            footer_note_y = margin - 0.02 * inch
            draw_box(
                margin,
                footer_note_y,
                page_w - 2 * margin,
                0.32 * inch,
                lw=0.8,
            )

            c.setFont("Helvetica", 7.5)
            c.drawString(
                margin + 8,
                footer_note_y + 0.18 * inch,
                "By opting in, you agree Karman Kar Shows & Events may contact you about this event and future events.",
            )
            c.drawString(
                margin + 8,
                footer_note_y + 0.06 * inch,
                "If selected, sponsor information may also be sent. Msg/data rates may apply. Opt out anytime.",
            )

            if mirror_back_pages:
                c.restoreState()

            c.showPage()

    c.save()
    buf.seek(0)
    return buf.getvalue()