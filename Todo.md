# Todo

## Roadmap

### Milestone: 0.8

- [ ] artifacts (replaces Pages)
- [ ] migration tool to leave sqlite backend
- [ ] repair day/entry mismatches
- [ ] paginate search results
- [ ] lazy load and export for filetree
- [ ] time ranges for question asking
- [x] improve LLM context and question answering
- [x] LLM integration with ChromaDB
- [x] web UI backed by filetree
- [x] remove tags

### Milestone: onboarding

- [ ] produce installation videos
- [ ] produce usage video
- [ ] installers - windows setup.exe and osx .pkg for Python/virtualenv
- [ ] integration for Debian/Ubuntu-flavored Linux
- [ ] integration for Redhat/Fedora-flavored Linux
- [ ] homebrew install
- [x] Docker workflow
- [x] powerpoint presentation
- [x] produce overview video

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

### Milestone: activity

- [ ] journal activity summary widget: daily, weekly
- [x] agenda widget extracts todo items from a day's entries
  - [x] render separately at bottom of day
- [ ] recent project activity widget (maybe project-system)
  - [ ] possibly from RSS

### Milestone: reports

- [ ] report report
- [ ] weather report
- [ ] git report
- [ ] headlines report
- [ ] systems report
- [ ] today's calendar report

### Milestone: next steps

- [ ] vscode extension could embed gthnk browser

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

### Milestone: simplify 0.7.0

- [x] update documentation and website to reflect current feature set
- [x] migration to update user table; rename email--username
- [x] tests passing
- [x] generate unique secret key when configuration is generated
- [x] logging during journal rotation
- [x] fix wrapping on long unbroken lines like URLs
- [x] hash passwords
- [x] results page displays as gthnk-card(s)
- [x] change password in gthnk.py, src/docker/bin/gthnk-user-password.sh
- [x] remove flask-diamond, refactor for simplicity

### Milestone: ui/ux

- [x] endpoint to view current configuration
- [x] keyboard hot keys: left, right, esc
- [x] swipe left/right
- [x] dark mode theme
- [x] improvement: remove /admin prefix on URLs
- [x] improvement: narrow screen rendering
- [x] automatically poll buffer for updates
- [x] quick add note in hamburger menu; append journal-web.txt with auto timestamp
  - [x] live view should stitch entries together and sort by time

