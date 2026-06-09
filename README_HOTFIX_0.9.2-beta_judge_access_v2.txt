Hotfix 0.9.2-beta v2 - Optional Judge Access Template Fix

Problem:
Railway showed a Jinja TemplateSyntaxError on /admin/shows/<id> because the restricted voting block in templates/admin_show_detail.html opened an if statement but did not close it before endblock.

Fix:
- Adds the missing {% endif %} for the restricted_voting_enabled block.
- Keeps judge access optional and available when participant/judge restricted voting is enabled.
- Does not remove the judge access feature.

Validation:
python -m py_compile app.py database.py utils/print_cards.py

Suggested commit:
git add app.py database.py templates README_HOTFIX_0.9.2-beta_judge_access_v2.txt
git commit -m "Hotfix 0.9.2-beta fix optional judge access template block"
git push origin main
