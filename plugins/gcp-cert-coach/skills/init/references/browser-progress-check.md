# Browser progress check

Reads which activities and modules the learner completed on Google Skills or Coursera, proposes completion marks, and writes nothing until the learner confirms. (The same procedure is in the progress skill.)

## Fallbacks first

| Situation | What to do |
|---|---|
| No built-in browser in this conversation | Say the check needs the Claude desktop app's built-in browser. Offer two options: open this chat in the desktop app, or type the progress (for example "courses 1, 3, 4; course 6 modules 1-3"). |
| The page asks to sign in (sign-in form, "Sign in to continue", a login redirect) | Ask the learner to sign in in the browser pane themselves, then retry once they say it is done. Never type credentials. Write nothing meanwhile. |
| The page does not look like a progress page (error, different course, empty list) | Show what you read in two or three lines and ask whether to retry, open a different page, or enter progress manually. |
| The learner declines | Use typed progress. |

## Reading progress

1. Open the provider page from `settings.path.providers` (or the activity `urls`):
   - Google Skills: the path page `https://www.skills.google/paths/<id>` and, for module detail, each activity page under it. Completed items show a completion mark or 100% progress; read page text rather than screenshots.
   - Coursera: the learner's specialization or course page (signed in). Completed modules show as completed.
2. Match activities and modules by title (ignore case and punctuation); report items you could not match instead of guessing.
3. Read only completion state. Do not store anything else from the account pages (names, emails, badges, dates other than completion).

## Proposal and confirmation

Show a table: activity, module, state on the site, proposed mark (completed / unchanged). Ask "Apply these marks?" Apply only after a yes, as one batch that sets `completed: true` and `completedAt` (today, or the site's completion date when shown) on each confirmed module. Never clear a mark because the site does not show it; ask instead.
