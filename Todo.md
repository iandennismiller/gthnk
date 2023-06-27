## Requested

- repair day/entry mismatches
- lazy load and export for filetree
- migration tool to leave sqlite backend
- LLM
  - [ ] Ask LLM function in web ui
  - [ ] time ranges for question asking
  - [ ] add dates to entries, include today's date in prompt
  - [ ] token frequency over time; surface to focus time ranges
  - [ ] split entries by paragraph for chromadb
  - [ ] Summarize each entry, day, week
  - [ ] summarize previous week/month/year
  - [ ] classify each entry and paragraph, store as chroma metadata
  - [ ] provide list of todo files, summarize and combine
- artifacts (replaces Pages)
- onboarding
  - [ ] produce installation videos
  - [ ] produce usage video
  - [ ] installers - windows setup.exe and osx .pkg for Python/virtualenv
  - [ ] integration for Debian/Ubuntu-flavored Linux
  - [ ] integration for Redhat/Fedora-flavored Linux
  - [ ] homebrew install
  - [x] Docker workflow
  - [x] powerpoint presentation
  - [x] produce overview video
- progressive web app
  - [ ] favicon, icon for web app
  - [ ] assemble day view from JSON via browser DOM
  - [ ] use service worker to broker day data
  - [ ] describe with manifest.json
  - [ ] PWA status bar should be consistent with theme (dark)
  - [ ] PWA startup window should be dark theme too
- journal activity summary widget: daily, weekly
- brainstorm reports idea (weather, git, systems, headlines, report report)

## To Do

- dockerfile updates
- what was in first-run?
- remove password and stuff?
- documentation updates

## Doing


## Waiting


## Done

- integration for Windows
- refresh documentation with new installation procedures
- testing for View components
- code coverage
- basic testing for Model components
- testing for Librarian
- rename OS X integration services
- bug: fix date picker
- bug: image attachments not centering
- write release procedure document
- tests pass again on Python 3
- rc1 to pypi
- consolidate javascript
- riot/matrix channel
- longer timeout for website authentication
- separate static content from template content
- fill out changelog
- write contributing document
- update documentation and website to reflect current feature set
- migration to update user table; rename email--username
- tests passing
- generate unique secret key when configuration is generated
- logging during journal rotation
- fix wrapping on long unbroken lines like URLs
- hash passwords
- results page displays as gthnk-card(s)
- change password in gthnk.py, src/docker/bin/gthnk-user-password.sh
- remove flask-diamond, refactor for simplicity
- endpoint to view current configuration
- keyboard hot keys: left, right, esc
- swipe left/right
- dark mode theme
- improvement: remove /admin prefix on URLs
- improvement: narrow screen rendering
- automatically poll buffer for updates
- quick add note in hamburger menu; append journal-web.txt with auto timestamp
- live view should stitch entries together and sort by time
- paginate web search results
- web UI backed by filetree
- remove tags
- try cascading simpler models (e.g. summarize context)
- improve LLM context and question answering
- LLM integration with ChromaDB
- agenda widget extracts todo items from a day's entries; render separately at bottom of day
- other cli things that should be tested?
- move "nearest day" to core gthnk, out of web
- test coverage for search
- test coverage
