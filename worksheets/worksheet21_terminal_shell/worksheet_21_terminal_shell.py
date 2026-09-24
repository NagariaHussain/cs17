"""Worksheet 21 - Terminal & Shell: the Media Club Archive.

The first worksheet in the module that is done entirely at a real terminal. The
student is handed `cs17-archive.zip`, extracts it, and tidies the mess inside it
with commands only - no mouse.

The sheet is ordered as **one tidy-up**, not as a tour of the command list: the
parts are the steps somebody actually takes when clearing out a messy folder,
and each command is met at the moment that step needs it.

  Part 1  look at the mess         pwd, ls, ls -l, ls -a, cd, .., ~, cat
  Part 2  build the shelves        mkdir, mkdir -p, and its two errors
  Part 3  move everything in       Tab, quoting, *, mv, cp
  Part 4  throw out what is left   rm, rmdir, --help, man, case, safety
  Part 5  find things and count    history, grep, wc
  Part 6  join commands up         |, >, >>, touch, echo, cowsay
  Part 7  save your history        history > history.txt, submission/, zip -r

Folders first is the load-bearing decision. The archive ships with **no** tidy
destination in it - no gallery, no backup, no sorted - so every folder Part 3
moves things into is one the student built in Part 2, and deleting in Part 4 is
something they can reason about, because by then a leftover is visibly a
leftover. Making a file only to move it two tasks later (the old shape) taught
the commands in the wrong order for the job.

Absolute-vs-relative is the module's main mental model, so it gets a written
drill of its own (the PATHS table in Part 1) on top of the cd tasks.

The parts are strictly cumulative and will not survive being done out of order:
Part 3 moves into folders Part 2 made, Part 4 deletes folders Part 3 emptied,
Part 6 counts what Part 3 put there, and Part 7 hands in files Part 6 wrote.

The map of the archive is deliberately **not** printed on the worksheet. It
lives in the archive's own README.txt; Part 1 has the student print it with
`cat` and copy it into a box by hand, which is the sheet's first real use of
the terminal as a source of truth. The answer key does print it, for marking.

Everything the sheet says about the archive - the tree, how many .jpg files a
wildcard picks up, what `wc -l` prints, how many lines `grep` matches - is
derived from ARCHIVE below, so the hand-out zip and the answer key can never
drift apart.
"""

from gens.termgen import (
    D, F, IMG, PART, TASK, PATHS, ERRORS, PREDICT, BOX,
    ascii_tree, find, listing, match, ngrep, nlines, text,
)

TITLE = "Worksheet 21: Terminal & Shell"
ZIP_NAME = "cs17-archive.zip"

# README.txt carries a map of the archive, but the map is drawn from the very
# tree README.txt sits in - so the file is authored with this placeholder line
# and the real tree is substituted once ARCHIVE exists (just below it). The
# substitution cannot change the map, because ascii_tree reads names only.
TREE_MARK = "{TREE}"


# ---- the archive the student receives ----------------------------------------
# Names are chosen to make the shell's rough edges show up on purpose:
#   - long names (club-members-attendance-register.txt) force Tab completion
#   - a folder with spaces ("Unsorted Camera Dump") forces quoting or escaping
#   - no two names differ only in case: macOS and Windows would silently
#     merge them on extraction (see tree.check_case_collisions). Case is
#     taught through commands, options and grep instead, which are case
#     sensitive everywhere
#   - inbox/competitions/photography-... is three deep, so ../../.. is needed
#   - inbox/old-phone-photos/ and documents/temp/ are rubbish that SHIPS in the
#     zip: Part 4 deletes folders the archive arrived with, never a folder the
#     student was asked to create
#   - there is NO tidy destination in the zip: no gallery/, no backup/, no
#     sorted/. Part 2 is the student making every one of them with mkdir, so
#     the folders they move into in Part 3 are folders they built themselves

MEMBERS = ["Aisha", "Rohan", "Meera", "Zaid", "Kavya", "Ibrahim"]
DATES = ["2026-01-07", "2026-01-14", "2026-01-21", "2026-02-04", "2026-02-11"]

_attendance = ["date,member,status"] + [
    f"{date},{member},{'absent' if (d + m) % 4 == 0 else 'present'}"
    for d, date in enumerate(DATES)
    for m, member in enumerate(MEMBERS)
]

_week_tests = {
    "01": ["camera timer test - SUCCESS", "night mode test - FAILED",
           "tripod balance test - SUCCESS", "battery life test - SUCCESS",
           "microphone test - FAILED"],
    "02": ["colour balance test - SUCCESS", "rain cover test - FAILED",
           "zoom lens test - FAILED", "drone flight test - SUCCESS",
           "sound sync test - SUCCESS"],
    "03": ["green screen test - FAILED", "lighting rig test - SUCCESS",
           "slow motion test - SUCCESS", "time lapse test - SUCCESS",
           "battery swap test - SUCCESS"],
    "04": ["editing export test - SUCCESS", "subtitle test - FAILED",
           "poster print test - SUCCESS", "projector test - FAILED",
           "final screening test - SUCCESS"],
}

_logs = [
    F(f"experiment-log-week-{wk}.txt",
      [f"CS17 Media Club - experiment log, week {int(wk)}"]
      + [f"Day {i}: {t}" for i, t in enumerate(tests, 1)])
    for wk, tests in _week_tests.items()
]

ARCHIVE = D("cs17-archive", [
    F("README.txt", [
        "CS17 Media Club - Archive",
        "=========================",
        "This folder is the club archive. It is a mess.",
        "Photographs are dumped in inbox. Reports and minutes are in documents.",
        "The experiment logs are in logs.",
        "There is nowhere tidy to put any of it. No gallery, no backup, no",
        "sorted folder. You make those yourself, before you move anything.",
        "Your job is to tidy it up from the terminal. Do not use the mouse.",
        "",
        "What is inside, on the day you got it",
        "-------------------------------------",
        TREE_MARK,
        "",
        "Copy this map onto your worksheet before you change anything. Later",
        "tasks ask you for paths, and the map is the quickest way to work one",
        "out without walking the folders with cd.",
        "",
        "The map is a photograph, not a live view. Every file that you move,",
        "copy or delete makes it older. When the map and ls disagree, ls is",
        "right.",
        "",
        "Last tidied: never.",
    ]),
    F("notes.txt", [
        "notes.txt - the everyday notes file. Anyone in the club may edit it.",
        "Type the name exactly as ls shows it, capitals and all.",
        "Some computers are fussy about that and some are not. Do not gamble.",
    ]),
    F("club-members-attendance-register.txt", _attendance),
    D("inbox", [
        # made by somebody two years ago and never used. It ships empty, so it
        # is the one folder on the sheet that rmdir takes on the first try.
        D("old-phone-photos", []),
        D("Unsorted Camera Dump", [
            IMG("IMG_0001.jpg", size=(640, 480), colour="#3b6ea5", label="ground"),
            IMG("IMG_0002.jpg", size=(800, 600), colour="#6a8f3d", label="field day"),
            IMG("IMG_0003.jpg", size=(720, 540), colour="#a5563b", label="workshop"),
            IMG("IMG_0004.jpg", size=(640, 480), colour="#4b3ba5", label="assembly"),
            IMG("IMG_0005.jpg", size=(960, 720), colour="#3ba58f", label="science fair"),
            IMG("IMG_0006.jpg", size=(800, 600), colour="#a53b6e", label="prize giving"),
            IMG("scoreboard-screenshot.png", size=(1024, 640), colour="#22272e",
                label="scoreboard"),
            F("camera-settings-backup.txt", [
                "camera settings backup",
                "iso=400",
                "aperture=f/5.6",
                "shutter=1/125",
                "white-balance=daylight",
            ]),
        ]),
        D("competitions", [
            D("photography-competition-entries-2026", [
                IMG("entry-aisha-sunrise.jpg", size=(1024, 768), colour="#d98c3f",
                    label="sunrise"),
                IMG("entry-rohan-bridge.jpg", size=(1024, 768), colour="#4f6d7a",
                    label="old bridge"),
                IMG("entry-meera-street-cat.jpg", size=(900, 675), colour="#7a5c4f",
                    label="street cat"),
                F("entries-received.txt", [
                    "entry,member,title",
                    "entry-aisha-sunrise.jpg,Aisha,Sunrise over the ground",
                    "entry-rohan-bridge.jpg,Rohan,The old bridge",
                    "entry-meera-street-cat.jpg,Meera,Street cat at noon",
                ]),
            ]),
        ]),
    ]),
    D("documents", [
        D("reports", [
            F("term-1-science-fair-report.txt", [
                "Term 1 Science Fair Report",
                "--------------------------",
                "The club entered four projects this term.",
                "Two of them were built in Scratch by the junior team.",
                "The solar oven project came second.",
                "Total spend from the budget was 2400 rupees.",
                "The photographs from the fair are still sitting in the inbox.",
            ]),
            F("term-2-science-fair-report.txt", [
                "Term 2 Science Fair Report",
                "--------------------------",
                "The junior team built a maze game in Scratch.",
                "A deep scratch on the camera lens ruined two photographs.",
                "Scratch projects were shown on the big screen all afternoon.",
                "Total spend from the budget was 1800 rupees.",
                "The gallery folder is still empty. Somebody please fix that.",
            ]),
        ]),
        D("minutes", [
            F("meeting-minutes-2026-01-14.txt", [
                "Media Club - meeting minutes - 14 January 2026",
                "Present: Aisha, Rohan, Meera, Zaid",
                "1. Agreed to tidy the archive before the next fair.",
                "2. Budget request of 3000 rupees sent to the office.",
                "3. Aisha will collect the competition entries.",
            ]),
            F("meeting-minutes-2026-02-11.txt", [
                "Media Club - meeting minutes - 11 February 2026",
                "Present: Rohan, Meera, Kavya, Ibrahim",
                "1. The archive is still a mess. Nobody has done it.",
                "2. Budget approved: 2500 rupees.",
                "3. Kavya will photograph the screening.",
            ]),
        ]),
        D("drafts", [
            F("old-notes.txt", [
                "Old notes from last year.",
                "Keep these, but move them out of drafts.",
            ]),
            F("scrap.txt", ["delete me"]),
        ]),
        # left-over folders that came with the archive. Part 4 deletes these:
        # a tidy-up throws away somebody else's mess, not a folder the student
        # was told to make two pages earlier.
        D("temp", [
            F("untitled-1.txt", ["asdf", "test test", "ignore this file"]),
            D("New Folder", []),
        ]),
    ]),
    D("logs", _logs),
])

# Draw the map into README.txt now that there is a tree to draw. The map is the
# same one the worksheet prints in its front matter (latex._intro calls the same
# ascii_tree), so a student who runs `cat README.txt` sees, character for
# character, what is on the sheet - and the two cannot drift.
README_TREE = ascii_tree(ARCHIVE)
_readme = find(ARCHIVE, "README.txt")
_readme.body = _readme.body.replace(TREE_MARK, README_TREE)
assert TREE_MARK not in _readme.body, "README.txt lost its {TREE} placeholder"

# The last line of README.txt is an answer on the sheet, so read it back rather
# than typing it twice.
README_LAST = text(ARCHIVE, "README.txt").rstrip("\n").splitlines()[-1]


# ---- numbers the answer key needs, all read back out of ARCHIVE --------------
# Nothing below is typed by hand: if a log line or a member is edited above, the
# key follows. The one thing we cannot derive is the student's own home folder,
# so absolute paths are written with the ~ shortcut and a note to compare it
# against what pwd actually printed.

REG = "club-members-attendance-register.txt"
TERM2 = "documents/reports/term-2-science-fair-report.txt"
WEEK1 = "logs/experiment-log-week-01.txt"

N_ROOT = len(listing(ARCHIVE))
N_DUMP_JPG = len(match(ARCHIVE, "inbox/Unsorted Camera Dump/*.jpg"))
N_ENTRY_JPG = len(match(ARCHIVE,
                        "inbox/competitions/"
                        "photography-competition-entries-2026/*.jpg"))
N_LOGS = len(match(ARCHIVE, "logs/*.txt"))
N_ROOT_TXT = len(match(ARCHIVE, "*.txt"))
REG_LINES = nlines(ARCHIVE, REG)
_reg_lines = text(ARCHIVE, REG).splitlines()
REG_HEAD3 = "\n".join(_reg_lines[:3])       # what `head -3` prints
REG_TAIL3 = "\n".join(_reg_lines[-3:])      # what `tail -3` prints
REG_LINE10 = _reg_lines[9]                  # the last line plain `head` shows
REG_AISHA = ngrep(ARCHIVE, REG, "Aisha")
REG_PRESENT = ngrep(ARCHIVE, REG, "present")
REG_ABSENT = ngrep(ARCHIVE, REG, "absent")
LOG_LINES = nlines(ARCHIVE, "logs/*.txt")
LOG_WEEK_LINES = nlines(ARCHIVE, WEEK1)
WK1_SUCCESS = ngrep(ARCHIVE, WEEK1, "SUCCESS")
WK3_SUCCESS = ngrep(ARCHIVE, "logs/experiment-log-week-03.txt", "SUCCESS")
ALL_FAILED = ngrep(ARCHIVE, "logs/*.txt", "FAILED")
BUDGET_LINES = ngrep(ARCHIVE, "documents/reports/*.txt", "budget")

# The tidy archive the student ends up with is not in ARCHIVE - the student
# builds it - so the few counts that describe the END state are written as
# arithmetic on the shipped counts, not typed in. gallery ends up holding the
# camera-dump photographs plus the competition-2026 folder: the screenshot that
# was moved in with them is deleted again in Part 4.
#   N_DUMP_JPG + 1   entries that `ls gallery` prints in Parts 6 and 7

# Two spellings of the same folder, and they are not interchangeable.
# BASE is how the *student writes* an absolute path in the PATHS drill, where
# ~ is the taught shortcut for the home folder. PWD is what the *shell prints*:
# pwd never abbreviates, so an answer to a pwd task must not contain a ~. The
# student's own username is the one thing here that cannot be derived.
# The one answer on this sheet that is copied from a real run rather than
# derived: cowsay's art cannot be computed from the archive. Captured from
# `cowsay "CS17 Army ROCKS"` on ubuntu:24.04, spacing and backslashes exactly
# as the student's terminal prints them.
COW = r"""
 _________________
< CS17 Army ROCKS >
 -----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||"""[1:]

BASE = "~/Desktop/terminal-assignment/cs17-archive"
PWD = "/home/<your-name>/Desktop/terminal-assignment/cs17-archive"
DUMP = "inbox/Unsorted Camera Dump"
DEEP = "inbox/competitions/photography-competition-entries-2026"


LEAD = (
    r"\textbf{Tidy up the Media Club archive from the terminal.}\quad The "
    r"archive is a mess. Your task is to sort it out with commands only. Do "
    r"not use the mouse."
    r"\par\vspace{6pt}"
    r"You get one zip file. Task~1 gives you the exact commands that unpack "
    r"it. After that you type every move, copy, rename, search and count. You "
    r"do not need the mouse at any point in this assignment."
    r"\par\vspace{6pt}"
    r"The commands and the messages here are the ones your Ubuntu "
    r"laptop prints. Ubuntu runs the \emph{bash} shell. Another computer can "
    r"word the same message a little differently."
    r"\par\vspace{6pt}"
    r"\textbf{The assignment is one tidy-up, done in order.} First you look at "
    r"the mess. Then you build the empty folders that the tidy archive needs. "
    r"Then you move everything into them. Then you throw away what is left "
    r"over. Only then do you search, count and join commands together. Do the "
    r"parts in order: each part works on what the part before it left behind, "
    r"so a part done out of turn will not have the folders or the files that "
    r"it needs."
    )


# Where the answers go is the one thing the printed sheet and the web page
# disagree about, so it is authored twice and each renderer takes its own.
ANSWER_NOTE = (
    r"Write your answers on this sheet as you work. The ruled lines, the box "
    r"in Part~1 and the tables are part of the task.")

ANSWER_NOTE_MD = (
    r"Write your answers in your own document as you work. Number each answer "
    r"with its part and its task number, for example 3.11. Copy the tables "
    r"into your document and fill them in there.")


HABITS = (
    r"\noindent\fbox{\begin{minipage}{0.96\linewidth}\small\vspace{2pt}"
    r"\textbf{Three habits. Use them from the first command to the last.}"
    r"\par\vspace{3pt}"
    r"\begin{itemize}"
    r"\item \textbf{Look before you act.} Run \cmd{pwd} and \cmd{ls} before "
    r"every command that copies, moves or deletes. There is no Undo. There is "
    r"no Trash."
    r"\item \textbf{Press Tab. Do not type the whole name.} Many names in this "
    r"archive are long. Type three letters, then press Tab."
    r"\item \textbf{Read the error.} An error message tells you what went "
    r"wrong. Read the whole line before you type the command again."
    r"\end{itemize}\vspace{2pt}\end{minipage}}")


# ---- Part 1: look at the mess ------------------------------------------------
# Orientation only. Nothing is created, moved or deleted here: the student
# opens the archive, learns to say where a file is, and copies the map out of
# README.txt. The map is the reference for every part after this one, which is
# why it is hand-copied rather than printed on the sheet.

p1 = PART(
    "Look at the mess",
    lesson="Lesson 1",
    intro=r"Ask two questions before every command. Where am I? What is here? "
          r"Each question has one command. You will type these two commands "
          r"more often than any other command in this assignment. In this part "
          r"you change nothing. You look, and you write down what you see.",
    recap=[
        ("pwd", "print the absolute path of the folder that you are in"),
        ("ls", "list the contents of this folder"),
        ("ls -l", "list with the size, the date and the permissions"),
        ("ls -a", "list all entries, including the hidden ones"),
        ("cd folder", "go into a folder"),
        ("cd ..", "go up one folder, to the parent"),
        ("cd ~", "go to your home folder"),
        ("cat file", "show the contents of a file on the screen"),
        ("unzip file.zip", "unpack a zip file into the folder that you are in"),
    ],
    tasks=[
        TASK(r"Open the terminal. The archive is in your \cmd{Downloads} "
             r"folder. Run these five commands, in this order. They make a "
             r"folder on your Desktop, move the zip into it, and unpack it. "
             r"You meet \cmd{mkdir}, \cmd{mv} and \cmd{cd} again later in this "
             r"assignment. \cmd{unzip} you need only here.",
             given="mkdir ~/Desktop/terminal-assignment\n"
                   "mv ~/Downloads/cs17-archive.zip ~/Desktop/terminal-assignment\n"
                   "cd ~/Desktop/terminal-assignment\n"
                   "unzip cs17-archive.zip\n"
                   "ls",
             expect="unzip prints one `inflating:` line for each file it "
                    "unpacks. The last command shows two entries: the zip and "
                    "the new cs17-archive folder.\n"
                    "If the shell answers `unzip: command not found`, install "
                    "it once with: sudo apt install unzip",
             hint=r"Add \cmd{-q} to \cmd{unzip} to unpack the archive quietly, "
                  r"with no list of files."),
        TASK(r"Go into the \cmd{cs17-archive} folder. Print the folder that you "
             r"are in. Copy the address exactly as the shell prints it.",
             cmd="cd ~/Desktop/terminal-assignment/cs17-archive\npwd",
             expect=f"{PWD}\n"
                    "It starts with / and leaves nothing out. A Mac prints "
                    "/Users/<your-name>/... instead of /home/<your-name>/..., "
                    "and the rest is the same.",
             write=1,
             hint=r"This address is the absolute path of the archive. Task~11 "
                  r"needs it again."),
        TASK(r"List the contents of the archive folder. How many items are "
             r"there?",
             cmd="ls",
             expect="   ".join(listing(ARCHIVE)) + "\n"
                    f"{N_ROOT} items. The order depends on the shell. Some "
                    "shells put the capital R of README.txt first. Some sort it "
                    "with the small letters.",
             write=1),
        TASK(r"List the folder again with the long details. Name two things "
             r"that the long listing shows and the plain listing does not.",
             cmd="ls -l",
             expect="Any two of these: the size in bytes, the date of the last "
                    "change, the owner, the permissions, and whether the entry "
                    "is a folder. A folder line starts with d.",
             write=2),
        TASK(r"List all entries, including the hidden ones. Write down one "
             r"entry that the earlier listings did not show.",
             cmd="ls -a",
             expect=".  and  ..  , this folder and its parent. A hidden name "
                    "starts with a dot.",
             write=1),
        TASK(r"Show \cmd{README.txt} on the screen. Do not open an "
             r"application. What is the last line?",
             cmd="cat README.txt",
             expect=README_LAST,
             write=1),
        BOX(r"\textbf{Copy the map.} \cmd{README.txt} holds a map of the "
            r"archive, and it is the only map you get: your worksheet does "
            r"not print one. Run \cmd{cat README.txt} again and copy the map "
            r"out by hand, exactly as the terminal prints it. Keep the "
            r"indentation. A name with a \cmd{/} after it is a folder; a name "
            r"without one is a file. Every part after this one asks you for "
            r"paths, and your copy is faster to read than \cmd{cd}.",
            # the map is 37 lines: at anything under ~4mm a line there is no
            # room to write it by hand, so the box takes most of a page.
            height=15.5,
            answer=README_TREE),
        TASK(r"Your map is a photograph of the archive as it was unpacked. "
             r"From Part~2 on you change the archive, so the map goes out of "
             r"date. Write down the one command that always tells you the "
             r"truth about a folder, whatever your map says.",
             expect="ls (with ls -l when you also want the sizes). The map is "
                    "a note on paper; ls asks the computer.",
             write=1),
        TASK(r"Show the Term~1 science fair report. Do not change folder "
             r"first. Use one command and one relative path. How many rupees "
             r"came out of the budget?",
             cmd="cat documents/reports/term-1-science-fair-report.txt",
             expect="2400 rupees.",
             write=1),
        TASK(r"Start in the archive folder. Go into the reports folder with one "
             r"command and a relative path. Print the folder to check the "
             r"result.",
             cmd="cd documents/reports\npwd",
             expect=f"{PWD}/documents/reports\n"
                    "pwd spells the home folder out. It never prints the ~ "
                    "shortcut, so this is longer than the path you would type.",
             write=1),
        TASK(r"Go back up from reports to the archive folder. Use one command.",
             cmd="cd ../..",
             expect="Two steps up: reports -> documents -> cs17-archive.",
             write=1),
        TASK(r"Start in the archive folder. Go into the deepest folder inside "
             r"\cmd{inbox} with one relative path. Press Tab for the long "
             r"names.",
             cmd=f"cd {DEEP}",
             expect="inbox -> competitions -> photography-competition-entries-2026",
             write=1),
        TASK(r"Stay in that deep folder. Go to the \cmd{logs} folder with a "
             r"relative path. Do not use \cmd{~}. Do not use an absolute path.",
             cmd="cd ../../../logs",
             expect="Three steps up to cs17-archive, then down into logs.",
             write=1),
        TASK(r"Go to your home folder. Then go back to the archive with one "
             r"command. Use the absolute path from task~2.",
             cmd="cd ~\ncd ~/Desktop/terminal-assignment/cs17-archive",
             expect="An absolute path works from any folder, because it does "
                    "not depend on where you are.",
             write=1),
        PATHS(
            caption=r"\textbf{The path drill.} Each row asks the same question "
                    r"two times. Write the relative path first. A relative path "
                    r"gives directions from the folder that you are in. Then "
                    r"write the absolute path. An absolute path is the full "
                    r"address and it starts at your home folder \cmd{~}. The "
                    r"archive is at "
                    r"\cmd{~/Desktop/terminal-assignment/cs17-archive}. Read "
                    r"the rows off the map that you copied.",
            rows=[
                ("cs17-archive", "logs", "logs", f"{BASE}/logs"),
                ("cs17-archive/logs", "cs17-archive/documents", "../documents",
                 f"{BASE}/documents"),
                ("documents/reports", "inbox", "../../inbox", f"{BASE}/inbox"),
                (f"{DUMP}", "logs", "../../logs", f"{BASE}/logs"),
                (f"{DEEP}", "documents/minutes", "../../../documents/minutes",
                 f"{BASE}/documents/minutes"),
                ("documents/minutes", "documents/reports", "../reports",
                 f"{BASE}/documents/reports"),
                ("documents/drafts", "cs17-archive", "..", BASE),
                ("anywhere at all", "your home folder", "(no relative path. It "
                 "depends on where you are)", "~"),
            ]),
        TASK(r"Read your finished table. Write one sentence about when to use a "
             r"relative path. Write one sentence about when to use an absolute "
             r"path.",
             expect="A relative path is shorter and it still works after "
                    "somebody moves or renames the whole archive. Use it for "
                    "short steps inside one project.\n"
                    "An absolute path always means the same one folder, from "
                    "anywhere. Use it to jump in from another part of the "
                    "computer.",
             write=3),
    ],
    note=r"\cmd{..} is not a normal folder. It is a shortcut and it always "
         r"means the folder above this one. \cmd{.} means this folder. "
         r"\cmd{ls -a} shows both of them.",
)


# ---- Part 2: build the shelves -----------------------------------------------
# Folders first, and nothing else. The archive ships with no tidy destination at
# all - no gallery, no backup - so every folder the later parts move things into
# is one the student makes here - and every folder made here is one a later
# part actually fills. Nothing is created to be deleted again: Part 4's targets
# (inbox/old-phone-photos, documents/temp, documents/drafts) all ship inside the
# zip, because throwing away somebody else's leftovers is the thing a tidy-up
# actually does.

p2 = PART(
    "Build the shelves",
    lesson="Lesson 1",
    intro=r"You cannot tidy a room with no shelves in it. The archive gives "
          r"you nowhere to put anything: there is no gallery, no backup and no "
          r"sorted folder. You make them, before you move a single file. One "
          r"command does it, and it is the same command in every part of this "
          r"assignment. Start in the archive folder and check with \cmd{pwd}.",
    recap=[
        ("mkdir name", "make a new folder"),
        ("mkdir a b c", "make several folders with one command"),
        ("mkdir one/two", "make two inside one, when one already exists"),
        ("mkdir -p one/two/three", "make every folder in the path that is missing"),
        ("ls", "check what you made"),
        ("ls -l", "a folder line starts with d"),
    ],
    tasks=[
        TASK(r"Make one folder in the archive folder with the name "
             r"\cmd{gallery}. Then list the archive folder to check it.",
             cmd="mkdir gallery\nls",
             expect=f"gallery is now in the listing. The archive holds "
                    f"{N_ROOT + 1} items."),
        TASK(r"Now try to make a folder inside a folder that does not exist "
             r"yet. Run \cmd{mkdir sorted/notes}. Copy the message. Why did "
             r"the command fail?",
             cmd="mkdir sorted/notes",
             expect="mkdir: cannot create directory 'sorted/notes': "
                    "No such file or directory\n"
                    "There is no sorted folder. mkdir makes one folder, the "
                    "last one in the path, and it will not invent the folders "
                    "above it.",
             write=2),
        TASK(r"Run the same command again with the \cmd{-p} option. Then list "
             r"the archive folder and \cmd{sorted}. How many folders did "
             r"\cmd{-p} make, and which ones?",
             cmd="mkdir -p sorted/notes\nls\nls sorted",
             expect="Two: sorted, and notes inside it. -p makes every folder "
                    "in the path that is missing, in one go.\n"
                    "Part 3 moves the club's notes into sorted/notes.",
             write=2),
        TASK(r"Two folders are still missing: \cmd{backup}, for a copy of the "
             r"experiment logs, and \cmd{competition-2026} inside "
             r"\cmd{gallery}, for the competition photographs. Make both with "
             r"\emph{one} command. You do not need \cmd{-p}: every folder "
             r"above them already exists.",
             cmd="mkdir backup gallery/competition-2026\nls\nls gallery",
             expect="mkdir takes as many names as you give it and makes every "
                    "one of them, so one command is enough.\n"
                    "gallery now holds competition-2026 and nothing else."),
        TASK(r"Run \cmd{mkdir gallery} a second time. Copy the message. Then "
             r"run \cmd{mkdir -p gallery} and say what is different.",
             cmd="mkdir gallery\nmkdir -p gallery",
             expect="mkdir: cannot create directory 'gallery': File exists\n"
                    "mkdir refuses, which is the safe answer: it will not touch "
                    "a folder that is already there and it will not empty it.\n"
                    "mkdir -p prints nothing and changes nothing. -p treats an "
                    "existing folder as a job already done.",
             write=2),
        TASK(r"List the archive folder. Write down the names of the three "
             r"folders that were not in the map you copied in Part~1. Then "
             r"say why \cmd{sorted/notes} is not one of the names you wrote.",
             cmd="ls\nls sorted\nls gallery",
             expect="gallery, backup and sorted are the three new names. The "
                    "rest of the listing is what came in the zip, unchanged.\n"
                    "sorted/notes is not in it because ls lists one folder, "
                    "not the folders inside it.",
             write=2),
        TASK(r"Look at your map from Part~1 again. It has two folders in it "
             r"that nothing in this assignment ever uses: "
             r"\cmd{inbox/old-phone-photos} and \cmd{documents/temp}. List "
             r"both of them and write down what is inside each one.",
             cmd='ls inbox/old-phone-photos\nls documents/temp',
             expect="inbox/old-phone-photos is empty: ls prints nothing at "
                    "all.\n"
                    "documents/temp holds untitled-1.txt and a folder called "
                    "New Folder, which is itself empty. Somebody made them "
                    "years ago and never came back.\n"
                    "These are the leftovers. Part 4 deletes them. Leave them "
                    "alone until then: you cannot tell rubbish from a "
                    "misplaced file until everything worth keeping has been "
                    "moved.",
             write=2),
    ],
    note=r"Make the folders before you move anything into them. \cmd{mv} and "
         r"\cmd{cp} do not create a destination: if you move a file into a "
         r"folder name that does not exist, the shell quietly renames the file "
         r"to that name instead, and the file is not where you think it is.",
)


# ---- Part 3: move in ---------------------------------------------------------
# The shelves from Part 2 get filled. Tab, quoting and * are taught here because
# this is the first part whose names are long enough and awkward enough to need
# them. mv for the tidy-up, cp only where the original has to stay.

p3 = PART(
    "Move everything into place",
    lesson="Lesson 2 and 3",
    intro=r"The shelves are up. Now carry the archive onto them. Two commands "
          r"do all of it. \cmd{mv} moves a file and leaves nothing behind, "
          r"which is what tidying up means. \cmd{cp} makes a second copy and "
          r"keeps the first, which is what a backup means. Three shortcuts "
          r"make the typing bearable: Tab finishes a name, quotes hold a name "
          r"with spaces together, and \cmd{*} stands for a whole group of "
          r"files. Start each task in the archive folder.",
    recap=[
        ("Tab", "finish the name that I started to type"),
        ('"name with spaces"', "quote a name so the shell reads it as one name"),
        ("*", "match any text here. *.jpg means every name that ends in .jpg"),
        ("mv from to", "move a file, or rename it"),
        ("cp from to", "copy a file and keep the original"),
        ("mv a b c folder/", "move several files into a folder with one command"),
        ("ls folder", "check the destination afterwards"),
    ],
    tasks=[
        TASK(r"Start in the archive folder. Type \cmd{cat club} and stop "
             r"there. Press Tab. Write the full name that the shell completes. "
             r"Then press Enter and look at the file.",
             cmd="cat club<Tab>     ->     cat club-members-attendance-register.txt",
             expect="club-members-attendance-register.txt. You typed 8 "
                    "characters and not 38. You also cannot spell the name "
                    "wrong.",
             write=1),
        TASK(r"Go into \cmd{documents/minutes}. Type "
             r"\cmd{cat meeting-minutes-2026-0} and press Tab. Nothing "
             r"happens. Press Tab a second time. Explain why the first Tab did "
             r"not complete the name.",
             cmd="cd documents/minutes\ncat meeting-minutes-2026-0<Tab><Tab>",
             expect="Two files start with those letters, ...-2026-01-14.txt and "
                    "...-2026-02-11.txt. The shell cannot know which one you "
                    "mean. The second Tab lists both files. You then type one "
                    "more character and press Tab again.",
             write=2),
        TASK(r"Go back to \cmd{inbox}. Enter the \cmd{Unsorted Camera Dump} "
             r"folder in three ways. Write the result of each one. "
             r"(a)~Type the name with no quotes and no Tab, then copy the "
             r"error. (b)~Put the whole name in double quotes. (c)~Type "
             r"\cmd{Uns} and press Tab, then copy what Tab typed for you.",
             cmd='cd ~/Desktop/terminal-assignment/cs17-archive/inbox\n'
                 'cd Unsorted Camera Dump        # fails\n'
                 'cd "Unsorted Camera Dump"      # works\n'
                 'cd Uns<Tab>                    # becomes: cd Unsorted\\ Camera\\ Dump',
             expect="(a) bash: cd: too many arguments\n"
                    "The shell split the name at the spaces. It read three "
                    "separate arguments.\n"
                    "(b) This works. The quotes join the words into one name.\n"
                    "(c) Tab puts a backslash before each space. A backslash "
                    "does the same job as the quotes.",
             write=3),
        TASK(r"Go back to the archive folder. List every \cmd{.jpg} file "
             r"inside the camera dump without going into it. How many are "
             r"there? Which two files in that folder does the pattern miss?",
             cmd=f'cd ~/Desktop/terminal-assignment/cs17-archive\n'
                 f'ls inbox/"Unsorted Camera Dump"/*.jpg',
             expect=f"{N_DUMP_JPG} files, IMG_0001.jpg to IMG_000{N_DUMP_JPG}.jpg.\n"
                    "The pattern misses scoreboard-screenshot.png and "
                    "camera-settings-backup.txt. A .png and a .txt do not end "
                    "in .jpg.",
             write=2),
        TASK(r"Move every one of those \cmd{.jpg} files into \cmd{gallery} "
             r"with one command. Then list both folders. Why is the camera "
             r"dump not empty yet?",
             cmd=f'mv inbox/"Unsorted Camera Dump"/*.jpg gallery/\n'
                 f'ls gallery\nls inbox/"Unsorted Camera Dump"',
             expect=f"gallery now holds {N_DUMP_JPG} photographs and the "
                    "competition-2026 folder.\n"
                    "The dump still holds the .png and the .txt, because *.jpg "
                    "did not match them. mv moved the files and left nothing "
                    "behind, so the photographs are in one place only.",
             write=1),
        TASK(r"The screenshot is a picture too. Move "
             r"\cmd{scoreboard-screenshot.png} into \cmd{gallery}. Press Tab "
             r"instead of typing that name.",
             cmd=f'mv inbox/"Unsorted Camera Dump"/scoreboard-screenshot.png gallery/',
             expect=f"gallery now holds {N_DUMP_JPG + 1} pictures and the "
                    "competition-2026 folder."),
        TASK(r"\cmd{camera-settings-backup.txt} is not a picture. It is a "
             r"note. Move it into \cmd{sorted/notes}. Then list the camera "
             r"dump. What does the shell print for an empty folder?",
             cmd=f'mv inbox/"Unsorted Camera Dump"/camera-settings-backup.txt '
                 f'sorted/notes/\nls inbox/"Unsorted Camera Dump"',
             expect="Nothing at all. ls prints an empty line for an empty "
                    "folder: no message, no error. The folder itself is still "
                    "there, and Part 4 deletes it.",
             write=1),
        TASK(r"Move the three competition entries into "
             r"\cmd{gallery/competition-2026}. Use one command and a "
             r"\cmd{*} pattern. Leave \cmd{entries-received.txt} where it is: "
             r"it is the record of who entered, not a photograph.",
             cmd=f"mv {DEEP}/*.jpg gallery/competition-2026/\n"
                 f"ls gallery/competition-2026\nls {DEEP}",
             expect=f"{N_ENTRY_JPG} entries in gallery/competition-2026.\n"
                    "entries-received.txt is the only thing left in the "
                    "competition folder."),
        TASK(r"The experiment logs must stay in \cmd{logs} and a copy must go "
             r"into \cmd{backup}. Use one command. Which of \cmd{mv} and "
             r"\cmd{cp} is the correct one here, and why?",
             cmd="cp logs/*.txt backup/\nls logs\nls backup",
             expect=f"cp. All {N_LOGS} logs are now in both folders. mv would "
                    "have emptied logs, and a backup that is the only copy is "
                    "not a backup.",
             write=2),
        TASK(r"Move \cmd{old-notes.txt} from \cmd{documents/drafts} into "
             r"\cmd{sorted/notes}.",
             cmd="mv documents/drafts/old-notes.txt sorted/notes/",
             expect="The file is no longer in drafts. It is now in sorted/notes."),
        TASK(r"Rename that file to \cmd{last-year-notes.txt}. Keep it in "
             r"\cmd{sorted/notes}.",
             cmd="mv sorted/notes/old-notes.txt sorted/notes/last-year-notes.txt",
             expect="A rename uses the same command as a move. mv changes the "
                    "name, the place, or both."),
        TASK(r"Copy the Term~2 report into \cmd{sorted/notes}. The original "
             r"must stay in \cmd{documents/reports}.",
             cmd="cp documents/reports/term-2-science-fair-report.txt sorted/notes/\n"
                 "ls documents/reports\nls sorted/notes",
             expect="The report is now in both folders. cp does not change the "
                    "original."),
        TASK(r"You used \cmd{mv} for the photographs and \cmd{cp} for the "
             r"logs and the report. Write the difference in one sentence. Then "
             r"write which command a tidy-up needs and which command a backup "
             r"needs.",
             expect="cp keeps the original and makes a second copy. mv leaves "
                    "nothing behind.\n"
                    "A tidy-up needs mv: a tidy archive does not keep the same "
                    "photograph in two places. A backup needs cp.",
             write=2),
        TASK(r"List \cmd{sorted/notes} with the long details. Which file is "
             r"the biggest? How do you know?",
             cmd="ls -l sorted/notes",
             expect="term-2-science-fair-report.txt. Its number in the size "
                    "column is the largest.",
             write=1),
    ],
    note=r"The shell expands \cmd{*}, not the command. The shell hands "
         r"\cmd{mv} all six filenames before \cmd{mv} starts. For this reason, "
         r"run \cmd{ls} with a pattern before you use that same pattern with a "
         r"command that moves or deletes: \cmd{ls} shows you exactly what the "
         r"other command is about to receive.",
)


# ---- Part 4: throw out what is left ------------------------------------------
# Deleting comes last of the three actions on purpose: by now every folder is
# either full of the right things or provably empty, so the student can see
# *why* a thing is rubbish rather than being told. The help / error / case /
# safety drills live here because this is the part where a mistake costs
# something.

p4 = PART(
    "Throw out what is left over",
    lesson="Lesson 2 and 5",
    intro=r"Everything worth keeping is on a shelf. What is left is either "
          r"rubbish or an empty folder that nothing lives in. Deleting is the "
          r"last step of a tidy-up and never the first, because before the "
          r"move you cannot tell a rubbish file from a file in the wrong "
          r"place. There is no Trash and there is no Undo, so every delete in "
          r"this part comes after \cmd{pwd} and \cmd{ls}.",
    recap=[
        ("rm file", "delete a file. There is no Trash and no Undo"),
        ("rmdir folder", "delete a folder, but only if the folder is empty"),
        ("pwd", "run this before a command that deletes. Where am I?"),
        ("ls", "run this before a command that deletes. Is that the right file?"),
        ("command --help", "ask a command to list its own options"),
        ("man command", "open the full manual. Press q to quit"),
    ],
    tasks=[
        TASK(r"\cmd{documents/drafts} still holds \cmd{scrap.txt}, and the "
             r"file says \cmd{delete me}. Run the two check commands from the "
             r"habits box first, then delete it. Write all three commands on "
             r"the lines below.",
             cmd="pwd\nls documents/drafts\nrm documents/drafts/scrap.txt",
             expect="pwd shows that you are in cs17-archive. ls shows that the "
                    "file is the correct one. Then rm deletes it, permanently.",
             write=3),
        TASK(r"\cmd{documents/drafts} is now empty. Delete the empty folder.",
             cmd="ls documents/drafts\nrmdir documents/drafts",
             expect="drafts disappears. rmdir works because the folder is "
                    "empty: you moved old-notes.txt out in Part 3 and deleted "
                    "scrap.txt a moment ago."),
        TASK(r"Part~3 emptied the camera dump. Delete that folder. The name "
             r"has spaces in it, so quote it or press Tab.",
             cmd=f'rmdir inbox/"Unsorted Camera Dump"\nls inbox',
             expect="competitions, and nothing else. The mess that the whole "
                    "assignment started with is gone, and no file was lost: "
                    "every one of them is on a shelf you made in Part 2."),
        TASK(r"\cmd{inbox/old-phone-photos} came with the archive and has been "
             r"empty since the day somebody made it. Delete it. This is the "
             r"only folder on this sheet that needs no preparation at all.",
             cmd="ls inbox/old-phone-photos\nrmdir inbox/old-phone-photos\nls inbox",
             expect="ls prints nothing, so the folder is empty and rmdir "
                    "accepts it straight away.\n"
                    "inbox is left with Unsorted Camera Dump and competitions."),
        TASK(r"\cmd{documents/temp} is the other leftover. It holds "
             r"\cmd{untitled-1.txt}, which says \cmd{asdf}, and an empty "
             r"folder called \cmd{New Folder}. Nobody has touched either for "
             r"years. Empty the folder: delete the file, then delete "
             r"\cmd{New Folder}. Its name has a space in it.",
             cmd='ls documents/temp\nrm documents/temp/untitled-1.txt\n'
                 'rmdir documents/temp/"New Folder"',
             expect="The quotes hold the two words together, exactly as they "
                    "did for Unsorted Camera Dump in Part 3. Tab does the same "
                    "job with a backslash.\n"
                    "documents/temp is now empty."),
        TASK(r"Now delete \cmd{documents/temp} itself. You could not have run "
             r"this command two tasks ago. Write down why, in one sentence.",
             cmd="rmdir documents/temp\nls documents",
             expect="reports, minutes, drafts.\n"
                    "rmdir refuses a folder that is not empty, so the file and "
                    "the folder inside temp had to go first. A folder tree "
                    "comes apart from the inside out. (rmdir -p "
                    "documents/temp/'New Folder' would have done the last two "
                    "steps in one command, for the same reason that mkdir -p "
                    "made two folders in Part 2.)",
             write=2),
        TASK(r"Try to delete \cmd{documents} with the same command. Copy the "
             r"message from the shell. Explain why the command failed, and why "
             r"this refusal is a good thing.",
             cmd="rmdir documents",
             expect="rmdir: failed to remove 'documents': Directory not empty\n"
                    "rmdir deletes empty folders only. This is a safety rule. "
                    "It stops one short command from taking the reports and "
                    "the minutes with the folder.",
             write=2),
        TASK(r"Try to delete the competition folder, "
             r"\cmd{inbox/competitions/photography-competition-entries-2026}. "
             r"It fails. Read the message, then answer: should you make it "
             r"empty so that the command works?",
             cmd=f'rmdir {DEEP}',
             expect="rmdir: failed to remove '...photography-competition-"
                    "entries-2026': Directory not empty\n"
                    "No. entries-received.txt is still in there and it is the "
                    "record of who entered the competition. The folder is not "
                    "left over, it is in use. rmdir refusing is the computer "
                    "telling you that you have not finished thinking.",
             write=2),
        TASK(r"The scoreboard screenshot is not a photograph of the club. It "
             r"is a picture of a screen and nobody wants it in the gallery. "
             r"Delete \cmd{gallery/scoreboard-screenshot.png}. Write the two "
             r"check commands that come before the delete, then run all three.",
             cmd="pwd\nls gallery\nrm gallery/scoreboard-screenshot.png",
             expect=f"gallery now holds {N_DUMP_JPG} photographs and the "
                    "competition-2026 folder.\n"
                    "This one is permanent in a way the others were not: you "
                    "moved this file in Part 3, so there is no second copy "
                    "anywhere. pwd and ls first, every time.",
             write=3),
        TASK(r"Run \cmd{ls --help}. The page is long. Do not read all of it. "
             r"Find the line for one option that you already use, and write "
             r"that line down.",
             cmd="ls --help",
             expect="The first line is `Usage: ls [OPTION]... [FILE]...`. Then "
                    "comes one line for each option, for example:\n"
                    "  -a, --all       do not ignore entries starting with .\n"
                    "  -l              use a long listing format\n"
                    "Not every command has --help. On a Mac, ls does not. Use "
                    "man when --help fails.",
             write=1),
        TASK(r"Open the manual for \cmd{rmdir}. Find out what \cmd{-p} does "
             r"there. Write the answer in your own words. Press \cmd{q} to "
             r"quit.",
             cmd="man rmdir",
             expect="-p removes the folder and then its parent folders too, as "
                    "long as each one becomes empty. It is the delete that "
                    "matches mkdir -p.",
             write=2),
        ERRORS(
            caption=r"\textbf{Break it on purpose.} Start in the archive "
                    r"folder. Run each line exactly as it is written. Copy the "
                    r"important part of the message from the shell. Then write "
                    r"in a few words why the command failed. Every line here "
                    r"fails safely: none of them deletes anything.",
            rows=[
                ("cd documets",
                 "bash: cd: documets: No such file or directory",
                 "The folder name is mistyped. Tab prevents this."),
                ("cd notes.txt",
                 "bash: cd: notes.txt: Not a directory",
                 "notes.txt is a file. You cannot go inside a file."),
                ("cat notes",
                 "cat: notes: No such file or directory",
                 "`.txt` is part of the name. The shell does not add it."),
                ("cp missing.txt backup/",
                 "cp: cannot stat 'missing.txt': No such file or directory",
                 "You cannot copy a file that is not there."),
                ("rm gallery",
                 "rm: cannot remove 'gallery': Is a directory",
                 "rm deletes files. A folder needs rmdir."),
                ("rmdir logs",
                 "rmdir: failed to remove 'logs': Directory not empty",
                 "rmdir deletes empty folders only."),
                ("mkdir sorted",
                 "mkdir: cannot create directory 'sorted': File exists",
                 "The folder is already there. mkdir will not touch it."),
            ]),
        TASK(r"Capital letters, part one. This part is the same on every "
             r"computer. Run \cmd{ls -l}. Then run \cmd{ls -L}. The letter is "
             r"the same and the case is different. Are the two listings the "
             r"same?",
             cmd="ls -l\nls -L",
             expect="No. -l gives the long listing. -L is a different option "
                    "and it follows shortcuts, so you get the short listing "
                    "back.\n"
                    "The command reads its own options, not the filesystem. So "
                    "options are case sensitive on every computer. The word "
                    "that you give to grep is case sensitive too.",
             write=2),
        TASK(r"Capital letters, part two. Names. Run \cmd{cat NOTES.txt}. "
             r"Then run a command name in capitals, \cmd{LS}. Copy both "
             r"messages. The file \cmd{notes.txt} is there and the command "
             r"\cmd{ls} exists, so why does Ubuntu refuse both?",
             cmd="cat NOTES.txt\nLS",
             expect="cat: NOTES.txt: No such file or directory\n"
                    "bash: LS: command not found\n"
                    "Ubuntu treats NOTES.txt and notes.txt as two different "
                    "names, and LS and ls as two different commands.\n"
                    "A Mac or a Windows laptop often accepts both, because it "
                    "ignores capitals in names. Ubuntu never does, and neither "
                    "does a server. Type every name the way ls shows it.",
             write=2),
        TASK(r"A command failed and you do not know why. Write the five checks "
             r"that you make, in order, before you ask for help.",
             expect="1. Where am I? -> pwd\n"
                    "2. What is here? -> ls\n"
                    "3. Is the name exact? -> check the spelling, the capitals "
                    "and the spaces\n"
                    "4. What does the command say? -> --help or man\n"
                    "5. Run the command again with the corrected path or name.",
             write=5),
    ],
    note=r"You can find \cmd{rm -rf} on the internet. Do not use it. It "
         r"deletes a whole folder tree and it asks no questions. In the wrong "
         r"folder it deletes your work. A tidy-up done in the right order "
         r"never needs it: move everything worth keeping first, and what is "
         r"left is empty folders and rubbish that \cmd{rm} and \cmd{rmdir} "
         r"handle one at a time.",
)


# ---- Part 5: find and count --------------------------------------------------
# Searching comes after the tidy-up, not before: grep and wc are asked questions
# about an archive that is now in a known shape, and every number here is read
# back out of ARCHIVE so the key cannot drift. This part also introduces
# history, which Part 7 turns into the hand-in file.

p5 = PART(
    "Find things and count them",
    lesson="Lesson 3",
    intro=r"The archive is tidy. Now use it. Two commands answer almost every "
          r"question about a text file without opening it: \cmd{grep} shows "
          r"the lines that contain a word, and \cmd{wc} counts. The shell also "
          r"remembers every command that you have typed today, which saves you "
          r"typing the long ones a second time. Start in the archive folder.",
    recap=[
        ("history", "list the commands that you ran"),
        ("Up / Down", "move back and forward through earlier commands"),
        ("clear", "clear the screen. Ctrl+L does the same"),
        ("head file", "show the first 10 lines of a file"),
        ("tail file", "show the last 10 lines of a file"),
        ("head -3 file", "show the first 3 lines. tail -3 shows the last 3"),
        ("grep word file", "show every line of the file that contains word"),
        ("grep word *.txt", "search a whole group of files at once"),
        ("wc file", "count the lines, words and bytes"),
        ("wc -l file", "count the lines only"),
    ],
    tasks=[
        TASK(r"Show the commands that you have run so far. How many commands "
             r"did the shell record? Then press the Up arrow to find the "
             r"\cmd{pwd} from Part~1 and run it again without typing it.",
             cmd="history",
             expect="The number at the left of the last line. Up and Down move "
                    "through the same list. You can also edit a line before "
                    "you press Enter.\n"
                    "Keep this terminal window open. Part 7 saves this list "
                    "into a file and hands it in, and a new window starts a "
                    "new list.",
             write=1),
        TASK(r"Clear the screen. Your commands are still there. Press the Up "
             r"arrow to check.",
             cmd="clear",
             expect="clear clears the display only. The history does not change."),
        PREDICT(
            caption=r"\textbf{Predict before you press Enter.} Start in the "
                    r"archive folder. Write what you expect each line to "
                    r"print. Then run the line and correct your answer. The "
                    r"archive is the tidy one that Parts~2 to~4 left behind.",
            rows=[
                ("ls *.txt",
                 f"the {N_ROOT_TXT} .txt files in the archive folder itself. "
                 "The shell does not search the subfolders"),
                ("ls *.jpg",
                 "ls: cannot access '*.jpg': No such file or directory. Nothing "
                 "in the archive folder matches, so bash hands the * to ls "
                 "unchanged"),
                ("ls gallery/*.jpg",
                 f"the {N_DUMP_JPG} photographs that you moved in Part 3, with "
                 "gallery/ in front of each name"),
                ("ls inbox/*",
                 "photography-competition-entries-2026. inbox holds only "
                 "competitions now, and ls lists what is inside it"),
                ("ls logs/*week-0*",
                 f"all {N_LOGS} experiment logs. A * can also stand in the "
                 "middle of a pattern"),
            ]),
        TASK(r"The attendance register is far too long to read on the screen. "
             r"Show the beginning of it with \cmd{head}. Do not give the "
             r"command any number. How many lines did it print, and what is "
             r"the first one?",
             cmd=f"head {REG}",
             expect=f"10 lines. That is what head prints when you do not ask "
                    f"for a number.\n"
                    f"The first line is the header, {_reg_lines[0]}, which "
                    f"names the three columns. The tenth is {REG_LINE10}.",
             write=2),
        TASK(r"Show the first three lines only. Then show the last three "
             r"lines. Write down the date on the last line of the file.",
             cmd=f"head -3 {REG}\ntail -3 {REG}",
             expect=f"head -3:\n{REG_HEAD3}\n\ntail -3:\n{REG_TAIL3}\n\n"
                    f"The last meeting in the register is "
                    f"{_reg_lines[-1].split(',')[0]}. head counts from the "
                    "top, tail counts from the bottom, and the number after "
                    "the dash is how many lines you want.",
             write=1),
        TASK(r"In Part~1 you used \cmd{cat} to find the last line of "
             r"\cmd{README.txt} and then read down the whole file to get to "
             r"it. Print that line again with one command that shows nothing "
             r"else.",
             cmd="tail -1 README.txt",
             expect=f"{README_LAST}\n"
                    "tail -1 is the shortest way to ask a file how it ends. "
                    "cat had to print the whole map first.",
             write=1),
        TASK(r"Look at the top of each experiment log with one command. "
             r"\cmd{head} takes a \cmd{*} pattern like the other commands. How "
             r"does it keep the four answers apart?",
             cmd="head -1 logs/*.txt",
             expect="It prints a ==> filename <== heading above each file, the "
                    "same idea as the filename grep puts in front of a "
                    "matching line.\n"
                    "The four headings are the week 1 to week 4 title lines.",
             write=1),
        TASK(r"Write one sentence. The logs are short, so \cmd{cat} works on "
             r"them. Why would you still reach for \cmd{head} or \cmd{tail} "
             r"on a file you do not know?",
             expect="Because cat prints the whole file however long it is. On "
                    "a file with thousands of lines that floods the screen and "
                    "scrolls the part you wanted out of sight. head and tail "
                    "show you the shape of a file first, and cost nothing on a "
                    "short one.",
             write=2),
        TASK(r"Search the week~1 experiment log for the word \cmd{SUCCESS}. "
             r"How many days passed?",
             cmd=f"grep SUCCESS {WEEK1}",
             expect=f"{WK1_SUCCESS} lines. grep shows the whole line, not the "
                    "word only.",
             write=1),
        TASK(r"Search all four logs with one command. Which week has the most "
             r"days with \cmd{SUCCESS}?",
             cmd="grep SUCCESS logs/*.txt",
             expect=f"Week 3, with {WK3_SUCCESS} days. With more than one file, "
                    "grep puts the filename in front of every matching line.",
             write=2),
        TASK(r"Search the Term~2 report for \cmd{Scratch} with a capital S. "
             r"Then search it for \cmd{scratch} with a small s. Are the lines "
             r"the same? What does this show about \cmd{grep}?",
             cmd=f"grep Scratch {TERM2}\ngrep scratch {TERM2}",
             expect=f"Capital S gives {ngrep(ARCHIVE, TERM2, 'Scratch')} lines, "
                    "about the programming. Small s gives "
                    f"{ngrep(ARCHIVE, TERM2, 'scratch')} line, about the camera "
                    "lens.\n"
                    "grep is case sensitive on every computer, whatever the "
                    "filesystem does with filenames. The two searches are two "
                    "different questions.",
             write=2),
        TASK(r"Count the lines, words and bytes in the attendance "
             r"register. Write the three numbers. Which number is the count of "
             r"register entries?",
             cmd=f"wc {REG}",
             expect=f"The first number is the line count, {REG_LINES}. The "
                    f"register holds {REG_LINES - 1} entries and 1 header line.",
             write=1),
        TASK(r"Count the lines only. Then find how many lines contain "
             r"\cmd{Aisha}. Count them by hand from the output of grep.",
             cmd=f"wc -l {REG}\ngrep Aisha {REG}",
             expect=f"{REG_LINES} lines in total. {REG_AISHA} of them contain "
                    "Aisha, one line for each meeting date.",
             write=2),
        TASK(r"Count the lines in all four logs with one command. What is the "
             r"total? Where does the shell show the total?",
             cmd="wc -l logs/*.txt",
             expect=f"{LOG_WEEK_LINES} lines in each log and {LOG_LINES} in "
                    "total. wc adds a `total` line at the bottom when you give "
                    "it several files.",
             write=1),
        TASK(r"Your backup was made with \cmd{cp} in Part~3. Count the lines "
             r"in \cmd{backup} the same way. Should the total match the one "
             r"from the task before?",
             cmd="wc -l backup/*.txt",
             expect=f"Yes, {LOG_LINES} again. cp copies the contents, so a "
                    "backup that does not match the original is a backup that "
                    "went wrong.",
             write=1),
    ],
    note=r"\cmd{grep} searches inside files. \cmd{ls} with a \cmd{*} searches "
         r"names. Two different questions: \emph{which file is called this} "
         r"and \emph{which file says this}.",
)


# ---- Part 6: join commands up ------------------------------------------------
# Pipes and redirection, no longer flagged as next week's lesson: the tidy-up
# has produced things worth counting, so | and > have a job. cowsay is in here
# because a pipeline whose last stage draws a cow is a pipeline a student will
# actually run twice, and it makes the point that the shell does not care what
# is on either side of the |.

p6 = PART(
    "Join commands up: pipes, files and a cow",
    lesson="Lesson 4",
    intro=r"Each command that you know does one small job. \cmd{cat} shows a "
          r"file. \cmd{grep} selects lines. \cmd{wc} counts. The shell joins "
          r"these jobs end to end, so that the output of one command becomes "
          r"the input of the next command:"
          r"\par\vspace{6pt}"
          r"\hspace*{1em}\cmd{INPUT}\quad$\rightarrow$\quad\cmd{COMMAND}"
          r"\quad$\rightarrow$\quad\cmd{OUTPUT}"
          r"\par\vspace{6pt}"
          r"\cmd{|} passes the output to another command. \cmd{>} writes the "
          r"output into a file instead of the screen. \cmd{>>} adds the output "
          r"to the end of a file. This is also where the files that you hand "
          r"in come from: every one of them is the output of a command, caught "
          r"in a file instead of printed. Predict the result of each line "
          r"before you press Enter.",
    recap=[
        ("a | b", "give the output of a to b as input"),
        ("a > file", "write the output of a into file and replace the contents"),
        ("a >> file", "add the output of a to the end of file and keep the rest"),
        ("touch file", "make an empty file"),
        ('echo "text"', "show some text on the screen"),
        ("cowsay text", "draw a cow saying text"),
    ],
    tasks=[
        TASK(r"Show the week~1 experiment log. Pass the output to \cmd{grep} "
             r"so that only the \cmd{SUCCESS} lines appear.",
             cmd=f"cat {WEEK1} | grep SUCCESS",
             expect=f"The same {WK1_SUCCESS} lines as in Part 5. This time grep "
                    "did not open the file. It read the output of cat."),
        TASK(r"Add one more stage. The shell must print the number of "
             r"successful days and not the lines.",
             cmd=f"cat {WEEK1} | grep SUCCESS | wc -l",
             expect=f"{WK1_SUCCESS}. Three commands do three small jobs: show "
                    "the file, keep the matching lines, count what is left.",
             write=1),
        TASK(r"Write one sentence. What does the \cmd{|} do in that command?",
             expect="It takes the output of the command on its left and gives "
                    "it to the command on its right as input, instead of "
                    "showing it on the screen.",
             write=2),
        TASK(r"Make an empty file in the archive folder with the name "
             r"\cmd{tidy-up-log.txt}. Then show that it is there and that it "
             r"is empty.",
             cmd="touch tidy-up-log.txt\nls -l tidy-up-log.txt",
             expect="The size column says 0. touch makes a file with no "
                    "contents at all."),
        TASK(r"Write one line into that file. The line has your name and the "
             r"word \emph{tidied}. Then show the file to check it.",
             cmd='echo "Archive tidied by Aisha" > tidy-up-log.txt\n'
                 'cat tidy-up-log.txt',
             expect="Archive tidied by Aisha\n"
                    "The > sends the output of echo into the file and not to "
                    "the screen. It replaces the old contents of the file."),
        TASK(r"Save the listing of \cmd{gallery} into a file with the name "
             r"\cmd{gallery-list.txt}. Put the file in the archive folder. "
             r"Then show the file. How many lines does it have, and why is "
             r"one of them not a photograph?",
             cmd="ls gallery > gallery-list.txt\ncat gallery-list.txt",
             expect=f"{N_DUMP_JPG + 1} lines: the {N_DUMP_JPG} photographs and "
                    "the competition-2026 folder. ls lists a folder by name "
                    "like anything else.\n"
                    "The first command printed nothing on the screen, because "
                    "the output went into the file.",
             write=1),
        TASK(r"Add one line to the end of that file with the name of the "
             r"person who checked it. Do not delete the lines that are already "
             r"there. Then show the file.",
             cmd='echo "checked by Aisha" >> gallery-list.txt\ncat gallery-list.txt',
             expect=f"{N_DUMP_JPG + 2} lines now: the listing, then your line."),
        TASK(r"Run the same line again with a single \cmd{>} and not "
             r"\cmd{>>}. Then show the file. What happened to the names? Build "
             r"the file again in the correct way. Part~7 hands this file in.",
             cmd='echo "checked by Aisha" > gallery-list.txt\ncat gallery-list.txt\n'
                 '# build it again:\nls gallery > gallery-list.txt\n'
                 'echo "checked by Aisha" >> gallery-list.txt',
             expect="> deleted the whole file and wrote one line. >> adds and > "
                    "replaces. This is the most common way to lose a file by "
                    "accident.",
             write=2),
        TASK(r"How many test days failed in all four logs? Answer with one "
             r"command. Use \cmd{cat}, \cmd{grep} and \cmd{wc}.",
             cmd="cat logs/*.txt | grep FAILED | wc -l",
             expect=f"{ALL_FAILED}.",
             write=1),
        TASK(r"How many lines of the attendance register contain \cmd{Aisha}? "
             r"Do not print the lines. Save only the number into a file with "
             r"the name \cmd{aisha-count.txt}. Then show that file.",
             cmd=f"grep Aisha {REG} | wc -l > aisha-count.txt\ncat aisha-count.txt",
             expect=f"{REG_AISHA}. grep finds the lines, wc -l counts them, and "
                    "> puts the count in the file and not on the screen.",
             write=1),
        TASK(r"Now something that is not installed yet. \cmd{cowsay} draws a "
             r"cow with a speech bubble. Install it once with the first line, "
             r"then run the second. The install asks for your password and "
             r"prints nothing while you type it.",
             given="sudo apt install cowsay\n"
                   'cowsay "CS17 Army ROCKS"',
             expect=COW + "\n\n"
                    "The bubble grows to fit whatever you give it, and the "
                    "cow is drawn underneath in plain characters.\n"
                    "If apt answers `Unable to locate package`, run "
                    "`sudo apt update` once and install again.\n"
                    "cowsay installs into /usr/games, which is on the PATH of "
                    "an Ubuntu desktop. If the shell still answers `cowsay: "
                    "command not found` straight after a successful install, "
                    "run it as /usr/games/cowsay."),
        TASK(r"\cmd{cowsay} reads its input the same way \cmd{grep} and "
             r"\cmd{wc} do, so it can be the last stage of a pipeline. Make "
             r"the cow say how many things are in \cmd{gallery}. Use "
             r"\cmd{ls}, \cmd{wc -l} and \cmd{cowsay}, joined with two "
             r"\cmd{|}.",
             cmd="ls gallery | wc -l | cowsay",
             expect=f"A cow saying {N_DUMP_JPG + 1}.\n"
                    "Nothing in the first two commands knows that a cow exists. "
                    "Each one writes its output, and the shell hands that "
                    "output to whatever comes next.",
             write=1),
        TASK(r"A cow is text like any other text, so it can go into a file. "
             r"Send the cow to the end of \cmd{tidy-up-log.txt} instead of the "
             r"screen, then show the file. Your name line from task~5 must "
             r"still be at the top.",
             cmd='cowsay "The archive is tidy" >> tidy-up-log.txt\n'
                 'cat tidy-up-log.txt',
             expect="Your line first, then the cow, drawn in the file exactly "
                    "as it was drawn on the screen. >> added it and kept what "
                    "was already there."),
        PREDICT(
            caption=r"\textbf{One more prediction round.} Write your answer "
                    r"first. Then run the line and compare it with your answer.",
            rows=[
                ("cat logs/*.txt | wc -l", str(LOG_LINES)),
                (f"grep present {REG} | wc -l", str(REG_PRESENT)),
                (f"grep absent {REG} | wc -l", str(REG_ABSENT)),
                ("cat documents/reports/*.txt | grep budget | wc -l",
                 str(BUDGET_LINES)),
                ("ls gallery | wc -l", str(N_DUMP_JPG + 1)),
            ]),
    ],
    note=r"Read a pipeline from left to right, like a sentence: \emph{show the "
         r"logs, keep the failures, count them}. If a long pipeline gives a "
         r"strange result, remove the last stage and run it again. This shows "
         r"you what passes through the middle.",
)


# ---- Part 7: the history file and the hand-in --------------------------------
# The last part turns the session itself into a deliverable. `history` has been
# on the sheet since Part 5 precisely so that this is a use of something known,
# not a new command in the last five minutes of the assignment.

p7 = PART(
    "Save your history and hand in",
    lesson="Lesson 4",
    intro=r"Everything that you typed in this assignment is still in the "
          r"shell's history, and \cmd{history} prints it. A printed list is no "
          r"use to anybody, so you send it into a file instead, with the "
          r"\cmd{>} from Part~6. That file is what you hand in with the "
          r"archive: it is the record of how you tidied it, in your own "
          r"commands. Do this part last, in the same terminal window that you "
          r"have used all along.",
    recap=[
        ("history", "print every command that you ran in this window"),
        ("history > file", "put that list into a file instead of on the screen"),
        ("head -20 file", "show the first 20 lines of a file"),
        ("tail -20 file", "show the last 20 lines of a file"),
        ("mv a b c folder/", "move several files into a folder with one command"),
        ("zip -r name.zip folder", "pack a folder and everything inside it"),
    ],
    tasks=[
        TASK(r"Start in the archive folder and check it with \cmd{pwd}. Print "
             r"your command history one more time. It is long now, so show "
             r"only the last twenty lines. Use \cmd{history}, a \cmd{|} and "
             r"\cmd{tail}.",
             cmd="pwd\nhistory | tail -20",
             expect="The last twenty commands, each with its number. history "
                    "writes its list out like any other command, so tail can "
                    "cut it down.",
             write=1),
        TASK(r"Save the whole history into a file with the name "
             r"\cmd{history.txt}, in the archive folder. Nothing must appear "
             r"on the screen. Then count the lines in the file.",
             cmd="history > history.txt\nwc -l history.txt",
             expect="One line for each command that you have run in this "
                    "window since you opened it. The number is your own: a "
                    "student who mistyped more commands has more lines, and "
                    "that is fine.\n"
                    "If the file is nearly empty, you are in a terminal window "
                    "that you opened later. The history belongs to the window, "
                    "not to the computer.",
             write=1),
        TASK(r"Show the first ten lines of \cmd{history.txt}. Which command "
             r"from Part~1 is at the top?",
             cmd="head -10 history.txt",
             expect="The mkdir, mv, cd and unzip lines from task 1 of Part 1, "
                    "in the order that you ran them.",
             write=1),
        TASK(r"How many folders did you make in this whole assignment? Answer "
             r"it from the file, with one command: search \cmd{history.txt} "
             r"for \cmd{mkdir} and count the matching lines.",
             cmd="grep mkdir history.txt | wc -l",
             expect="Your own number. It counts the failed attempts too, "
                    "because the shell records what you typed and not what "
                    "worked. Part 2 alone had two mkdir commands that failed "
                    "on purpose.",
             write=1),
        TASK(r"Make a folder with the name \cmd{submission} inside "
             r"\cmd{cs17-archive}.",
             cmd="mkdir submission",
             expect="The last folder you make in this assignment, and the same "
                    "command as the first one in Part 2."),
        TASK(r"Move \cmd{gallery-list.txt}, \cmd{aisha-count.txt} and "
             r"\cmd{tidy-up-log.txt} into it. Use one command for all three "
             r"files. Leave \cmd{history.txt} in the archive folder.",
             cmd="mv gallery-list.txt aisha-count.txt tidy-up-log.txt submission/\nls",
             expect="mv takes several sources and one destination, and the "
                    "destination goes last. The archive folder now holds "
                    "history.txt and the folders, and the three files are in "
                    "submission."),
        TASK(r"Write your full name into \cmd{submission/name.txt}. Use one "
             r"command.",
             cmd='echo "Aisha Khan" > submission/name.txt',
             expect="echo with > writes the line straight into a new file. You "
                    "do not need touch first: > makes the file if it is not "
                    "there."),
        TASK(r"List \cmd{submission} with the long details. Check that four "
             r"files are there and that none of them is empty.",
             cmd="ls -l submission",
             expect="gallery-list.txt, aisha-count.txt, tidy-up-log.txt and "
                    "name.txt. Every size column is bigger than 0. A 0 means "
                    "you wrote the file with > twice and emptied it.",
             write=1),
    ],
    note=r"\cmd{history} belongs to the terminal window that you are in. Close "
         r"the window before you save the file and the list starts again from "
         r"nothing. Save \cmd{history.txt} before you close anything, and if "
         r"you did lose it, say so when you hand in rather than typing a fake "
         r"list: a short honest history is worth more than an invented one.",
)


PARTS = [p1, p2, p3, p4, p5, p6, p7]


CLOSING = (
    r"\subsection*{Hand in}"
    r"Part~7 built your hand-in. This is the last thing you do, and it is two "
    r"commands. Go up one folder, to \cmd{terminal-assignment}, and pack the "
    r"whole \cmd{cs17-archive} folder into a zip file with your own name in "
    r"the filename. \cmd{zip} is the partner of \cmd{unzip}, and \cmd{-r} "
    r"tells it to include every folder inside:"
    r"\par\vspace{6pt}"
    r"\hspace*{1em}\cmd{cd ~/Desktop/terminal-assignment}\par\vspace{2pt}"
    r"\hspace*{1em}\cmd{zip -r submission-your-name.zip cs17-archive}"
    r"\par\vspace{6pt}"
    r"Upload that zip file. Hand in this sheet with it."
    r"\par\vspace{6pt}"
    r"\noindent\fbox{\begin{minipage}{0.96\linewidth}\small\vspace{2pt}"
    r"\textbf{Check this list before you pack the zip.} Every line is "
    r"something you can check with \cmd{ls}."
    r"\par\vspace{3pt}"
    r"\begin{itemize}"
    r"\item \cmd{gallery} holds the six camera photographs and the "
    r"\cmd{competition-2026} folder, and the screenshot is gone."
    r"\item \cmd{gallery/competition-2026} holds the three competition entries."
    r"\item \cmd{backup} holds all four experiment logs, and \cmd{logs} still "
    r"holds them too."
    r"\item \cmd{sorted/notes} holds \cmd{last-year-notes.txt}, the copy of "
    r"the Term~2 report and \cmd{camera-settings-backup.txt}."
    r"\item Four folders that came in the zip are gone: "
    r"\cmd{documents/drafts}, \cmd{documents/temp}, "
    r"\cmd{inbox/old-phone-photos} and \cmd{inbox/Unsorted Camera Dump}."
    r"\item \cmd{history.txt} is in \cmd{cs17-archive} itself, not in "
    r"\cmd{submission}, and it is not empty."
    r"\item \cmd{submission} holds four files. One of them has your name."
    r"\item Every question, the map you copied in Part~1 and every table "
    r"has an answer."
    r"\end{itemize}\vspace{2pt}\end{minipage}}")


REFERENCE = [
    ("pwd", "show the folder that you are in"),
    ("ls", "list the contents of this folder"),
    ("ls -l", "list with the sizes and the dates"),
    ("ls -a", "list the hidden entries too"),
    ("cd", "change folder"),
    ("mkdir", "make a folder"),
    ("mkdir -p", "make every folder in the path that is missing"),
    ("touch", "make an empty file"),
    ("cat", "show the contents of a file"),
    ("cp", "copy a file"),
    ("mv", "move a file, or rename it"),
    ("rm", "delete a file. This is permanent"),
    ("rmdir", "delete an empty folder"),
    ("rmdir -p", "delete a folder and its parents, while each one is empty"),
    ("echo", "show text on the screen"),
    ("clear", "clear the screen"),
    ("history", "show the commands that you ran in this window"),
    ("head -n", "show the first n lines of a file"),
    ("tail -n", "show the last n lines of a file"),
    ("cowsay", "draw a cow saying something. It reads a pipe too"),
    ("grep", "show the lines of a file that contain a word"),
    ("wc", "count the lines, words and bytes"),
    ("wc -l", "count the lines only"),
    ("unzip", "unpack a zip file"),
    ("zip -r", "pack a folder and everything inside it into a zip file"),
    ("man", "open the manual of a command. Press q to quit"),
    ("--help", "ask a command to list its options"),
    (">", "write output into a file and replace the contents"),
    (">>", "add output to the end of a file"),
    ("|", "send the output of one command into another command"),
    ("*", "match any text here"),
    ("..", "the folder above this one"),
    ("~", "your home folder"),
    ('"name with spaces"', "one name, not several arguments"),
    ("Tab", "finish the name that I started to type"),
    ("Up / Down", "move through the commands that you ran"),
]


# ---- the cheat sheet ---------------------------------------------------------
# The card the student keeps next to the keyboard. It stands on its own: it
# carries no worksheet number, and it is deliberately NOT built out of the
# assignment archive, because a reference should still make sense in a year,
# long after cs17-archive and Worksheet 21 have been forgotten. Instead every example runs in one
# tiny made-up folder, ~/work, which is printed at the top of the card, so each
# line can be read on its own without hunting for what a file contains.
#
# Every output below was copied from a real Ubuntu 24.04 run of that folder,
# through a terminal (not a pipe), because `ls` lays names out in columns on a
# terminal and one per line into a pipe.

from gens.termgen.cheatsheet import SECTION, ENTRY, FIELDS   # noqa: E402

CHEAT_NAME = "terminal-shell-cheat-sheet"
CHEAT_TITLE = "Terminal & Shell Cheat Sheet"
CHEAT_SUBTITLE = "Ubuntu, bash"

_LSL = "-rw-rw-r-- 1 you you 59 Sep 15 10:30 notes.txt"
_WC = " 3 10 59 notes.txt"
_CP = "cp notes.txt backup/"
_LSO = "ls -l photos"

CHEAT_SHEET = [
    SECTION("The folder used in every example", [
        ENTRY("", "",
              ex="~/work/\n"
                 "|-- notes.txt    3 lines of text\n"
                 "|-- report.txt   2 lines of text\n"
                 "|-- todo.txt     4 lines, 3 of them start with buy\n"
                 "|-- photos/      cat.jpg  dog.jpg  tree.jpg\n"
                 "`-- backup/      empty",
              note="Make it yourself in two minutes and try every line on this "
                   "card."),
    ]),

    SECTION("How a command is built", [
        ENTRY("command argument argument", "what to do, then what to do it to",
              ex="$ " + _CP,
              ann=FIELDS(_CP, {0: "the command: what to do",
                               1: "what to do it to",
                               2: "where to put it"})),
        ENTRY("command option argument", "an option changes how it is done",
              ex="$ " + _LSO,
              ann=FIELDS(_LSO, {0: "the command",
                                1: "an option: how to do it",
                                2: "what to do it to"}),
              note="An option starts with <b>-</b> and is case sensitive. "
                   "<b>-l</b> and <b>-L</b> are different options."),
    ]),

    SECTION("Where am I, and what is here?", [
        ENTRY("pwd", "print the folder you are in",
              ex="$ pwd\n/home/you/work",
              note="It starts at <b>/</b> and leaves nothing out. That is an "
                   "<b>absolute path</b>."),
        ENTRY("ls", "list what is in a folder",
              ex="$ ls\nbackup  notes.txt  photos  report.txt  todo.txt\n"
                 "$ ls photos\ncat.jpg  dog.jpg  tree.jpg",
              note="No folder named? Then it lists the one you are in."),
        ENTRY("ls -l", "list with the details",
              ex="$ ls -l notes.txt\n" + _LSL,
              ann=FIELDS(_LSL, {0: "- = file, d = folder", 4: "size in bytes",
                                5: "when it changed"}),
              note="<b>you you</b> is your own username, twice."),
        ENTRY("ls -a", "list the hidden entries too",
              ex="$ ls -a photos\n.  ..  cat.jpg  dog.jpg  tree.jpg",
              note="<b>.</b> is this folder. <b>..</b> is the folder above it. "
                   "A hidden name starts with a dot."),
        ENTRY("cd folder", "go into a folder",
              ex="$ cd photos\n$ pwd\n/home/you/work/photos",
              note="<b>cd ..</b> goes up one. <b>cd ../..</b> goes up two. "
                   "<b>cd ~</b> goes home, and so does <b>cd</b> on its own."),
    ]),

    SECTION("Two ways to say where", [
        ENTRY("", "", rows=[
            ("photos", "<b>relative</b>: a folder inside the one I am in"),
            ("../report.txt", "<b>relative</b>: up one, then that file"),
            ("../../work", "<b>relative</b>: up two, then down into work"),
            ("~/work/photos", "<b>absolute</b>: start at my home folder"),
            ("/home/you/work", "<b>absolute</b>: start at the very top"),
        ], note="Relative is shorter, and it still works after the whole folder "
                "is moved. Absolute means the same one place from anywhere."),
    ]),

    SECTION("Make, read, copy, move, delete", [
        ENTRY("mkdir name", "make a folder",
              ex="$ mkdir letters\n$ mkdir letters/sent letters/draft",
              note="It takes as many names as you give it."),
        ENTRY("touch file", "make an empty file",
              ex="$ touch list.txt"),
        ENTRY("cat file", "show what is in a file",
              ex="$ cat notes.txt\nMeeting on Monday.\nBring the camera.\n"
                 "Ask about the budget."),
        ENTRY("head -n 2 file", "show only the first 2 lines",
              ex="$ head -n 2 notes.txt\nMeeting on Monday.\nBring the camera."),
        ENTRY("tail -n 1 file", "show only the last line",
              ex="$ tail -n 1 notes.txt\nAsk about the budget.",
              note="Change the number to get more lines. With no <b>-n</b> at "
                   "all, both show 10. For a file too long for <b>cat</b>."),
        ENTRY('echo "text"', "print text",
              ex='$ echo "Hello there"\nHello there'),
        ENTRY("cp from to", "copy it. The original stays",
              ex="$ cp notes.txt backup/\n$ ls backup\nnotes.txt"),
        ENTRY("mv from to", "move it, or rename it",
              ex="$ mv notes.txt backup/        moves it\n"
                 "$ mv notes.txt old-notes.txt  renames it",
              note="Both change the name or the place, so both are <b>mv</b>."),
        ENTRY("rm file", "delete a file. Permanently",
              ex="$ rm list.txt",
              note="<span class='danger'>No Trash. No Undo.</span> Run "
                   "<b>pwd</b> and <b>ls</b> first, every time."),
        ENTRY("rmdir folder", "delete a folder, if it is empty",
              ex="$ rmdir backup"),
        ENTRY("", "", box=True,
              note="<b>Silence means success.</b> mkdir, touch, cp, mv, rm and "
                   "rmdir print nothing when they work. If you see a message, "
                   "something went wrong. Read it."),
    ]),

    SECTION("Type less", [
        ENTRY("", "", rows=[
            ("Tab", "finish the name I started. Type 3 letters, press Tab"),
            ("Tab Tab", "nothing completed? Press again to see every match"),
            ("Up / Down", "step through the commands you already ran"),
            ("history", "list them all, with a number on each"),
            ("clear", "clear the screen. Ctrl+L does the same"),
            ("Ctrl+C", "stop a command that is still running"),
        ]),
        ENTRY('"name with spaces"', "quote it, or the shell reads two names",
              ex='$ cd My Photos\nbash: cd: too many arguments\n$ cd "My Photos"',
              note="Tab does it for you, with a <b>\\</b> before each space."),
        ENTRY("*", "match any text here",
              ex="$ ls photos/*.jpg\n"
                 "photos/cat.jpg  photos/dog.jpg  photos/tree.jpg",
              note="The <b>shell</b> expands <b>*</b> before the command runs. "
                   "Check what it matches before you attach it to <b>rm</b>."),
    ]),

    SECTION("Search inside files, and count", [
        ENTRY("grep word file", "print every line that contains word",
              ex="$ grep buy todo.txt\nbuy milk\nbuy bread\nbuy stamps",
              note="3 lines came out, so 3 of the 4 jobs are shopping. grep "
                   "prints the whole line, not the word. It is <b>case "
                   "sensitive</b>: <b>Buy</b> would find none of these."),
        ENTRY("grep word *.txt", "search several files at once",
              ex="$ grep buy *.txt\ntodo.txt:buy milk\ntodo.txt:buy bread\n"
                 "todo.txt:buy stamps",
              note="With more than one file it puts the filename in front, so "
                   "you can tell the hits apart."),
        ENTRY("wc file", "count lines, words and bytes",
              ex="$ wc notes.txt\n" + _WC,
              ann=FIELDS(_WC, {0: "lines", 1: "words", 2: "bytes"}),
              note="The third number is bytes, not letters. For plain English "
                   "text they are the same. A file with accents or emoji has "
                   "more bytes than letters, and <b>wc -m</b> counts the "
                   "letters."),
        ENTRY("wc -l file", "count the lines only",
              ex="$ wc -l *.txt\n  3 notes.txt\n  2 report.txt\n  4 todo.txt\n"
                 "  9 total",
              note="Several files? wc adds a <b>total</b> line at the bottom."),
    ]),

    SECTION("Join commands together", [
        ENTRY("a | b", "give what a printed to b as its input",
              ex="$ grep buy todo.txt | wc -l\n3",
              note="Read it left to right: <i>find the buy lines, count them</i>. "
                   "grep never opened a file for wc here."),
        ENTRY("a > file", "write the output into a file. Replaces it",
              ex="$ ls photos > list.txt\n$ cat list.txt\ncat.jpg\ndog.jpg\ntree.jpg",
              note="Nothing appears on screen when you run the first line. The "
                   "output went into the file."),
        ENTRY("a >> file", "add the output to the end. Keeps the rest",
              ex='$ echo "checked by me" >> list.txt',
              note="<b>&gt;&gt;</b> adds. <b>&gt;</b> replaces. Mixing them up "
                   "is the usual way to lose a file."),
    ]),

    SECTION("Putting it together", [
        ENTRY("", "",
              ex="$ cd ~/work\n"
                 "$ mkdir shopping\n"
                 "$ grep buy todo.txt > shopping/list.txt\n"
                 "$ cat shopping/list.txt\n"
                 "buy milk\nbuy bread\nbuy stamps\n"
                 "$ wc -l shopping/list.txt\n"
                 "3 shopping/list.txt\n"
                 "$ cp notes.txt shopping/\n"
                 "$ ls shopping\nlist.txt  notes.txt",
              note="Six commands, one job. Only the ones with something to "
                   "show printed anything."),
    ], intro="A real job, start to finish: pull the shopping lines out of "
             "<b>todo.txt</b>, count them, and keep a copy of the notes beside "
             "them."),

    SECTION("When it goes wrong", [
        ENTRY("", "", rows=[
            ("No such file or directory",
             "the name is wrong. Check the spelling, the capitals and the <b>.txt</b>"),
            ("Not a directory", "that is a file. You cannot <b>cd</b> into a file"),
            ("Directory not empty", "<b>rmdir</b> only removes empty folders"),
            ("too many arguments", "a name has spaces in it. Quote it"),
            ("command not found", "the command name is wrong. <b>LS</b> is not <b>ls</b>"),
            ("cannot access '*.png'", "nothing matched the <b>*</b>"),
            ("Permission denied", "the file is not yours to change. Leave it alone"),
        ]),
        ENTRY("ls --help", "ask a command to list its own options",
              ex="$ ls --help\nUsage: ls [OPTION]... [FILE]...\n"
                 "  -a, --all   do not ignore entries starting with .\n"
                 "  -l          use a long listing format",
              note="Long output? Try <b>ls --help | head -20</b>."),
        ENTRY("man ls", "the full manual for a command",
              ex="$ man ls",
              note="Arrow keys scroll. Press <b>q</b> to quit."),
        ENTRY("", "", box=True,
              note="<b>Stuck? Five checks, in order.</b> "
                   "1. Where am I? <b>pwd</b> &nbsp; "
                   "2. What is here? <b>ls</b> &nbsp; "
                   "3. Is the name exact? Check spelling, capitals, spaces. &nbsp; "
                   "4. What does <b>--help</b> or <b>man</b> say? &nbsp; "
                   "5. Try again with the corrected name."),
        ENTRY("", "", box=True,
              note="<b>Ubuntu counts capitals.</b> <b>notes.txt</b> and "
                   "<b>NOTES.txt</b> are two different names. <b>ls</b> and "
                   "<b>LS</b> are two different commands. Type every name the "
                   "way <b>ls</b> shows it."),
    ]),
]
