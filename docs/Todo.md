# Todo

## Milestone: simplify 0.7.x

- [ ] migration to update user table; rename email--username
- [ ] generate unique secret key when configuration is generated
- [ ] unified logging during journal rotation
- [ ] update documentation and website to reflect current feature set
- [ ] tests passing
- [x] fix wrapping on long unbroken lines like URLs
- [x] hash passwords
- [x] results page displays as gthnk-card(s)
- [x] change password in gthnk.py, src/docker/bin/gthnk-user-password.sh
- [x] remove flask-diamond, refactor for simplicity

## Milestone: attachments 0.8.x

- [ ] develop plan for attachments

## Milestone: onboarding

- [ ] produce installation videos
- [ ] produce usage video
- [ ] installers - windows setup.exe and osx .pkg for Python/virtualenv
- [ ] integration for Debian/Ubuntu-flavored Linux
- [ ] integration for Redhat/Fedora-flavored Linux
- [x] Docker workflow
- [x] powerpoint presentation
- [x] produce overview video

## Milestone: ui/ux

- [x] keyboard hot keys: left, right, esc
- [x] swipe left/right
- [x] dark mode theme
- [x] improvement: remove /admin prefix on URLs
- [x] improvement: narrow screen rendering
- [x] automatically poll buffer for updates
- [ ] endpoint to view current configuration

## Milestone: progressive web app

- [ ] favicon, icon for web app
- [ ] assemble day view from JSON via browser DOM
- [ ] use service worker to broker day data
- [ ] describe with manifest.json

## Milestone: code quality

- [ ] more robust testing of explorer attachments
- [ ] enable flake8 Dxxx checks
- [ ] testing for integration.py
- [ ] refactor javascript

## Milestone: tags

- [x] double-square-brackets: tagging, wiki-like pseudo-page results
  - [ ] list tags separate from fulltext results
- [ ] search auto-complete for tags
- [ ] timeline of when tags appear
- [ ] rethink /search as /tag/blah
- [ ] "search" becomes "go to"
- [ ] entry co-tag graph, navigator
- [ ] date filter on search/go to

## Milestone: activity

- [ ] journal activity summary widget: daily, weekly
- [x] agenda widget extracts todo items from a day's entries
  - [x] render separately at bottom of day
- [ ] recent project activity widget (maybe project-system)
  - [ ] possibly from RSS

## Ready for Upcoming Release

### Themes

- Focusing on the main idea: the journal.

### Items

- [x] integration for Windows
- [x] refresh documentation with new installation procedures
- [x] testing for View components
- [x] code coverage
- [x] basic testing for Model components
- [x] testing for Librarian
- [x] rename OS X integration services
- [x] bug: fix date picker
- [x] bug: image attachments not centering
- [x] write release procedure document
- [x] tests pass again on Python 3
- [x] rc1 to pypi
- [x] consolidate javascript
- [x] riot/matrix channel
- [N] longer timeout for website authentication
- [x] separate static content from template content
- [x] fill out changelog
- [x] write contributing document
