# Todo

## Roadmap

### Milestone: simplify 0.7.0

- [ ] update documentation and website to reflect current feature set
- [x] migration to update user table; rename email--username
- [x] tests passing
- [x] generate unique secret key when configuration is generated
- [x] logging during journal rotation
- [x] fix wrapping on long unbroken lines like URLs
- [x] hash passwords
- [x] results page displays as gthnk-card(s)
- [x] change password in gthnk.py, src/docker/bin/gthnk-user-password.sh
- [x] remove flask-diamond, refactor for simplicity

### Milestone: attachments 0.7.1

- [ ] develop plan for attachments

### Milestone: onboarding

- [ ] produce installation videos
- [ ] produce usage video
- [ ] installers - windows setup.exe and osx .pkg for Python/virtualenv
- [ ] integration for Debian/Ubuntu-flavored Linux
- [ ] integration for Redhat/Fedora-flavored Linux
- [x] Docker workflow
- [x] powerpoint presentation
- [x] produce overview video

### Milestone: ui/ux

- [x] keyboard hot keys: left, right, esc
- [x] swipe left/right
- [x] dark mode theme
- [x] improvement: remove /admin prefix on URLs
- [x] improvement: narrow screen rendering
- [x] automatically poll buffer for updates
- [ ] endpoint to view current configuration
- [ ] vscode extension could embed gthnk browser
- [ ] quick add note in hamburger menu; append journal-web.txt with auto timestamp

### Milestone: progressive web app

- [ ] favicon, icon for web app
- [ ] assemble day view from JSON via browser DOM
- [ ] use service worker to broker day data
- [ ] describe with manifest.json
- [ ] PWA status bar should be consistent with theme (dark)
- [ ] PWA startup window should be dark theme too

### Milestone: code quality

- [ ] more robust testing of explorer attachments
- [ ] enable flake8 Dxxx checks
- [ ] testing for integration.py
- [ ] refactor javascript

### Milestone: tags

- [x] double-square-brackets: tagging, wiki-like pseudo-page results
  - [ ] list tags separate from fulltext results
- [ ] search auto-complete for tags
- [ ] timeline of when tags appear
- [ ] rethink /search as /tag/blah
- [ ] "search" becomes "go to"
- [ ] entry co-tag graph, navigator
- [ ] date filter on search/go to

### Milestone: activity

- [ ] journal activity summary widget: daily, weekly
- [x] agenda widget extracts todo items from a day's entries
  - [x] render separately at bottom of day
- [ ] recent project activity widget (maybe project-system)
  - [ ] possibly from RSS

## Done

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
- [x] longer timeout for website authentication
- [x] separate static content from template content
- [x] fill out changelog
- [x] write contributing document
