# Worksheet 21: Terminal & Shell

*CS17 · cs17.org*

**Tidy up the Media Club archive from the terminal.** The archive is a mess. Your task is to sort it out with commands only. Do not use the mouse.

You get one zip file. Task 1 gives you the exact commands that unpack it. After that you type every move, copy, rename, search and count. You do not need the mouse at any point in this assignment.

The commands and the messages here are the ones your Ubuntu laptop prints. Ubuntu runs the *bash* shell. Another computer can word the same message a little differently.

**The assignment is one tidy-up, done in order.** First you look at the mess. Then you build the empty folders that the tidy archive needs. Then you move everything into them. Then you throw away what is left over. Only then do you search, count and join commands together. Do the parts in order: each part works on what the part before it left behind, so a part done out of turn will not have the folders or the files that it needs.

Write your answers in your own document as you work. Number each answer with its part and its task number, for example 3.11. Copy the tables into your document and fill them in there.

## What is inside `cs17-archive.zip`

Task 1 unpacks the zip. You get one folder with the name `cs17-archive`, and every file and folder in this assignment is inside it. The map of that folder is not printed here. It is inside the archive, in `README.txt`, and Part 1 asks you to print it and copy it out. Keep your copy beside you: most of the work in this assignment is to reach the correct place in that tree.

> **Three habits. Use them from the first command to the last.**
>
> - **Look before you act.** Run `pwd` and `ls` before every command that copies, moves or deletes. There is no Undo. There is no Trash.
> - **Press Tab. Do not type the whole name.** Many names in this archive are long. Type three letters, then press Tab.
> - **Read the error.** An error message tells you what went wrong. Read the whole line before you type the command again.

## Part 1. Look at the mess

*Lesson 1*

Ask two questions before every command. Where am I? What is here? Each question has one command. You will type these two commands more often than any other command in this assignment. In this part you change nothing. You look, and you write down what you see.

| Command | What it does |
|---|---|
| `pwd` | print the absolute path of the folder that you are in |
| `ls` | list the contents of this folder |
| `ls -l` | list with the size, the date and the permissions |
| `ls -a` | list all entries, including the hidden ones |
| `cd folder` | go into a folder |
| `cd ..` | go up one folder, to the parent |
| `cd ~` | go to your home folder |
| `cat file` | show the contents of a file on the screen |
| `unzip file.zip` | unpack a zip file into the folder that you are in |

1. Open the terminal. The archive is in your `Downloads` folder. Run these five commands, in this order. They make a folder on your Desktop, move the zip into it, and unpack it. You meet `mkdir`, `mv` and `cd` again later in this assignment. `unzip` you need only here.

   *Hint: Add `-q` to `unzip` to unpack the archive quietly, with no list of files.*

   ```text
   mkdir ~/Desktop/terminal-assignment
   mv ~/Downloads/cs17-archive.zip ~/Desktop/terminal-assignment
   cd ~/Desktop/terminal-assignment
   unzip cs17-archive.zip
   ls
   ```

2. Go into the `cs17-archive` folder. Print the folder that you are in. Copy the address exactly as the shell prints it.

   *Hint: This address is the absolute path of the archive. Task 11 needs it again.*

3. List the contents of the archive folder. How many items are there?

4. List the folder again with the long details. Name two things that the long listing shows and the plain listing does not.

5. List all entries, including the hidden ones. Write down one entry that the earlier listings did not show.

6. Show `README.txt` on the screen. Do not open an application. What is the last line?

**Copy the map.** `README.txt` holds a map of the archive, and it is the only map you get: your worksheet does not print one. Run `cat README.txt` again and copy the map out by hand, exactly as the terminal prints it. Keep the indentation. A name with a `/` after it is a folder; a name without one is a file. Every part after this one asks you for paths, and your copy is faster to read than `cd`.

7. Your map is a photograph of the archive as it was unpacked. From Part 2 on you change the archive, so the map goes out of date. Write down the one command that always tells you the truth about a folder, whatever your map says.

8. Show the Term 1 science fair report. Do not change folder first. Use one command and one relative path. How many rupees came out of the budget?

9. Start in the archive folder. Go into the reports folder with one command and a relative path. Print the folder to check the result.

10. Go back up from reports to the archive folder. Use one command.

11. Start in the archive folder. Go into the deepest folder inside `inbox` with one relative path. Press Tab for the long names.

12. Stay in that deep folder. Go to the `logs` folder with a relative path. Do not use `~`. Do not use an absolute path.

13. Go to your home folder. Then go back to the archive with one command. Use the absolute path from task 2.

**The path drill.** Each row asks the same question two times. Write the relative path first. A relative path gives directions from the folder that you are in. Then write the absolute path. An absolute path is the full address and it starts at your home folder `~`. The archive is at `~/Desktop/terminal-assignment/cs17-archive`. Read the rows off the map that you copied.

| You are in | You want to reach | Relative path | Absolute path |
|---|---|---|---|
| `cs17-archive` | `logs` |  |  |
| `cs17-archive/logs` | `cs17-archive/documents` |  |  |
| `documents/reports` | `inbox` |  |  |
| `inbox/Unsorted Camera Dump` | `logs` |  |  |
| `inbox/competitions/photography-competition-entries-2026` | `documents/minutes` |  |  |
| `documents/minutes` | `documents/reports` |  |  |
| `documents/drafts` | `cs17-archive` |  |  |
| `anywhere at all` | `your home folder` |  |  |

14. Read your finished table. Write one sentence about when to use a relative path. Write one sentence about when to use an absolute path.

> **Remember**
>
> `..` is not a normal folder. It is a shortcut and it always means the folder above this one. `.` means this folder. `ls -a` shows both of them.

## Part 2. Build the shelves

*Lesson 1*

You cannot tidy a room with no shelves in it. The archive gives you nowhere to put anything: there is no gallery, no backup and no sorted folder. You make them, before you move a single file. One command does it, and it is the same command in every part of this assignment. Start in the archive folder and check with `pwd`.

| Command | What it does |
|---|---|
| `mkdir name` | make a new folder |
| `mkdir a b c` | make several folders with one command |
| `mkdir one/two` | make two inside one, when one already exists |
| `mkdir -p one/two/three` | make every folder in the path that is missing |
| `ls` | check what you made |
| `ls -l` | a folder line starts with d |

1. Make one folder in the archive folder with the name `gallery`. Then list the archive folder to check it.

2. Now try to make a folder inside a folder that does not exist yet. Run `mkdir sorted/notes`. Copy the message. Why did the command fail?

3. Run the same command again with the `-p` option. Then list the archive folder and `sorted`. How many folders did `-p` make, and which ones?

4. Two folders are still missing: `backup`, for a copy of the experiment logs, and `competition-2026` inside `gallery`, for the competition photographs. Make both with *one* command. You do not need `-p`: every folder above them already exists.

5. Run `mkdir gallery` a second time. Copy the message. Then run `mkdir -p gallery` and say what is different.

6. List the archive folder. Write down the names of the three folders that were not in the map you copied in Part 1. Then say why `sorted/notes` is not one of the names you wrote.

7. Look at your map from Part 1 again. It has two folders in it that nothing in this assignment ever uses: `inbox/old-phone-photos` and `documents/temp`. List both of them and write down what is inside each one.

> **Remember**
>
> Make the folders before you move anything into them. `mv` and `cp` do not create a destination: if you move a file into a folder name that does not exist, the shell quietly renames the file to that name instead, and the file is not where you think it is.

## Part 3. Move everything into place

*Lesson 2 and 3*

The shelves are up. Now carry the archive onto them. Two commands do all of it. `mv` moves a file and leaves nothing behind, which is what tidying up means. `cp` makes a second copy and keeps the first, which is what a backup means. Three shortcuts make the typing bearable: Tab finishes a name, quotes hold a name with spaces together, and `*` stands for a whole group of files. Start each task in the archive folder.

| Command | What it does |
|---|---|
| `Tab` | finish the name that I started to type |
| `"name with spaces"` | quote a name so the shell reads it as one name |
| `*` | match any text here. *.jpg means every name that ends in .jpg |
| `mv from to` | move a file, or rename it |
| `cp from to` | copy a file and keep the original |
| `mv a b c folder/` | move several files into a folder with one command |
| `ls folder` | check the destination afterwards |

1. Start in the archive folder. Type `cat club` and stop there. Press Tab. Write the full name that the shell completes. Then press Enter and look at the file.

2. Go into `documents/minutes`. Type `cat meeting-minutes-2026-0` and press Tab. Nothing happens. Press Tab a second time. Explain why the first Tab did not complete the name.

3. Go back to `inbox`. Enter the `Unsorted Camera Dump` folder in three ways. Write the result of each one. (a) Type the name with no quotes and no Tab, then copy the error. (b) Put the whole name in double quotes. (c) Type `Uns` and press Tab, then copy what Tab typed for you.

4. Go back to the archive folder. List every `.jpg` file inside the camera dump without going into it. How many are there? Which two files in that folder does the pattern miss?

5. Move every one of those `.jpg` files into `gallery` with one command. Then list both folders. Why is the camera dump not empty yet?

6. The screenshot is a picture too. Move `scoreboard-screenshot.png` into `gallery`. Press Tab instead of typing that name.

7. `camera-settings-backup.txt` is not a picture. It is a note. Move it into `sorted/notes`. Then list the camera dump. What does the shell print for an empty folder?

8. Move the three competition entries into `gallery/competition-2026`. Use one command and a `*` pattern. Leave `entries-received.txt` where it is: it is the record of who entered, not a photograph.

9. The experiment logs must stay in `logs` and a copy must go into `backup`. Use one command. Which of `mv` and `cp` is the correct one here, and why?

10. Move `old-notes.txt` from `documents/drafts` into `sorted/notes`.

11. Rename that file to `last-year-notes.txt`. Keep it in `sorted/notes`.

12. Copy the Term 2 report into `sorted/notes`. The original must stay in `documents/reports`.

13. You used `mv` for the photographs and `cp` for the logs and the report. Write the difference in one sentence. Then write which command a tidy-up needs and which command a backup needs.

14. List `sorted/notes` with the long details. Which file is the biggest? How do you know?

> **Remember**
>
> The shell expands `*`, not the command. The shell hands `mv` all six filenames before `mv` starts. For this reason, run `ls` with a pattern before you use that same pattern with a command that moves or deletes: `ls` shows you exactly what the other command is about to receive.

## Part 4. Throw out what is left over

*Lesson 2 and 5*

Everything worth keeping is on a shelf. What is left is either rubbish or an empty folder that nothing lives in. Deleting is the last step of a tidy-up and never the first, because before the move you cannot tell a rubbish file from a file in the wrong place. There is no Trash and there is no Undo, so every delete in this part comes after `pwd` and `ls`.

| Command | What it does |
|---|---|
| `rm file` | delete a file. There is no Trash and no Undo |
| `rmdir folder` | delete a folder, but only if the folder is empty |
| `pwd` | run this before a command that deletes. Where am I? |
| `ls` | run this before a command that deletes. Is that the right file? |
| `command --help` | ask a command to list its own options |
| `man command` | open the full manual. Press q to quit |

1. `documents/drafts` still holds `scrap.txt`, and the file says `delete me`. Run the two check commands from the habits box first, then delete it. Write all three commands on the lines below.

2. `documents/drafts` is now empty. Delete the empty folder.

3. Part 3 emptied the camera dump. Delete that folder. The name has spaces in it, so quote it or press Tab.

4. `inbox/old-phone-photos` came with the archive and has been empty since the day somebody made it. Delete it. This is the only folder on this sheet that needs no preparation at all.

5. `documents/temp` is the other leftover. It holds `untitled-1.txt`, which says `asdf`, and an empty folder called `New Folder`. Nobody has touched either for years. Empty the folder: delete the file, then delete `New Folder`. Its name has a space in it.

6. Now delete `documents/temp` itself. You could not have run this command two tasks ago. Write down why, in one sentence.

7. Try to delete `documents` with the same command. Copy the message from the shell. Explain why the command failed, and why this refusal is a good thing.

8. Try to delete the competition folder, `inbox/competitions/photography-competition-entries-2026`. It fails. Read the message, then answer: should you make it empty so that the command works?

9. The scoreboard screenshot is not a photograph of the club. It is a picture of a screen and nobody wants it in the gallery. Delete `gallery/scoreboard-screenshot.png`. Write the two check commands that come before the delete, then run all three.

10. Run `ls --help`. The page is long. Do not read all of it. Find the line for one option that you already use, and write that line down.

11. Open the manual for `rmdir`. Find out what `-p` does there. Write the answer in your own words. Press `q` to quit.

**Break it on purpose.** Start in the archive folder. Run each line exactly as it is written. Copy the important part of the message from the shell. Then write in a few words why the command failed. Every line here fails safely: none of them deletes anything.

| Run this | What the shell printed | Why it failed |
|---|---|---|
| `cd documets` |  |  |
| `cd notes.txt` |  |  |
| `cat notes` |  |  |
| `cp missing.txt backup/` |  |  |
| `rm gallery` |  |  |
| `rmdir logs` |  |  |
| `mkdir sorted` |  |  |

12. Capital letters, part one. This part is the same on every computer. Run `ls -l`. Then run `ls -L`. The letter is the same and the case is different. Are the two listings the same?

13. Capital letters, part two. Names. Run `cat NOTES.txt`. Then run a command name in capitals, `LS`. Copy both messages. The file `notes.txt` is there and the command `ls` exists, so why does Ubuntu refuse both?

14. A command failed and you do not know why. Write the five checks that you make, in order, before you ask for help.

> **Remember**
>
> You can find `rm -rf` on the internet. Do not use it. It deletes a whole folder tree and it asks no questions. In the wrong folder it deletes your work. A tidy-up done in the right order never needs it: move everything worth keeping first, and what is left is empty folders and rubbish that `rm` and `rmdir` handle one at a time.

## Part 5. Find things and count them

*Lesson 3*

The archive is tidy. Now use it. Two commands answer almost every question about a text file without opening it: `grep` shows the lines that contain a word, and `wc` counts. The shell also remembers every command that you have typed today, which saves you typing the long ones a second time. Start in the archive folder.

| Command | What it does |
|---|---|
| `history` | list the commands that you ran |
| `Up / Down` | move back and forward through earlier commands |
| `clear` | clear the screen. Ctrl+L does the same |
| `head file` | show the first 10 lines of a file |
| `tail file` | show the last 10 lines of a file |
| `head -3 file` | show the first 3 lines. tail -3 shows the last 3 |
| `grep word file` | show every line of the file that contains word |
| `grep word *.txt` | search a whole group of files at once |
| `wc file` | count the lines, words and bytes |
| `wc -l file` | count the lines only |

1. Show the commands that you have run so far. How many commands did the shell record? Then press the Up arrow to find the `pwd` from Part 1 and run it again without typing it.

2. Clear the screen. Your commands are still there. Press the Up arrow to check.

**Predict before you press Enter.** Start in the archive folder. Write what you expect each line to print. Then run the line and correct your answer. The archive is the tidy one that Parts 2 to 4 left behind.

| Command | Write your prediction, then run the line |
|---|---|
| `ls *.txt` |  |
| `ls *.jpg` |  |
| `ls gallery/*.jpg` |  |
| `ls inbox/*` |  |
| `ls logs/*week-0*` |  |

3. The attendance register is far too long to read on the screen. Show the beginning of it with `head`. Do not give the command any number. How many lines did it print, and what is the first one?

4. Show the first three lines only. Then show the last three lines. Write down the date on the last line of the file.

5. In Part 1 you used `cat` to find the last line of `README.txt` and then read down the whole file to get to it. Print that line again with one command that shows nothing else.

6. Look at the top of each experiment log with one command. `head` takes a `*` pattern like the other commands. How does it keep the four answers apart?

7. Write one sentence. The logs are short, so `cat` works on them. Why would you still reach for `head` or `tail` on a file you do not know?

8. Search the week 1 experiment log for the word `SUCCESS`. How many days passed?

9. Search all four logs with one command. Which week has the most days with `SUCCESS`?

10. Search the Term 2 report for `Scratch` with a capital S. Then search it for `scratch` with a small s. Are the lines the same? What does this show about `grep`?

11. Count the lines, words and bytes in the attendance register. Write the three numbers. Which number is the count of register entries?

12. Count the lines only. Then find how many lines contain `Aisha`. Count them by hand from the output of grep.

13. Count the lines in all four logs with one command. What is the total? Where does the shell show the total?

14. Your backup was made with `cp` in Part 3. Count the lines in `backup` the same way. Should the total match the one from the task before?

> **Remember**
>
> `grep` searches inside files. `ls` with a `*` searches names. Two different questions: *which file is called this* and *which file says this*.

## Part 6. Join commands up: pipes, files and a cow

*Lesson 4*

Each command that you know does one small job. `cat` shows a file. `grep` selects lines. `wc` counts. The shell joins these jobs end to end, so that the output of one command becomes the input of the next command:

`INPUT` → `COMMAND` → `OUTPUT`

`|` passes the output to another command. `>` writes the output into a file instead of the screen. `>>` adds the output to the end of a file. This is also where the files that you hand in come from: every one of them is the output of a command, caught in a file instead of printed. Predict the result of each line before you press Enter.

| Command | What it does |
|---|---|
| `a \| b` | give the output of a to b as input |
| `a > file` | write the output of a into file and replace the contents |
| `a >> file` | add the output of a to the end of file and keep the rest |
| `touch file` | make an empty file |
| `echo "text"` | show some text on the screen |
| `cowsay text` | draw a cow saying text |

1. Show the week 1 experiment log. Pass the output to `grep` so that only the `SUCCESS` lines appear.

2. Add one more stage. The shell must print the number of successful days and not the lines.

3. Write one sentence. What does the `|` do in that command?

4. Make an empty file in the archive folder with the name `tidy-up-log.txt`. Then show that it is there and that it is empty.

5. Write one line into that file. The line has your name and the word *tidied*. Then show the file to check it.

6. Save the listing of `gallery` into a file with the name `gallery-list.txt`. Put the file in the archive folder. Then show the file. How many lines does it have, and why is one of them not a photograph?

7. Add one line to the end of that file with the name of the person who checked it. Do not delete the lines that are already there. Then show the file.

8. Run the same line again with a single `>` and not `>>`. Then show the file. What happened to the names? Build the file again in the correct way. Part 7 hands this file in.

9. How many test days failed in all four logs? Answer with one command. Use `cat`, `grep` and `wc`.

10. How many lines of the attendance register contain `Aisha`? Do not print the lines. Save only the number into a file with the name `aisha-count.txt`. Then show that file.

11. Now something that is not installed yet. `cowsay` draws a cow with a speech bubble. Install it once with the first line, then run the second. The install asks for your password and prints nothing while you type it.

    ```text
    sudo apt install cowsay
    cowsay "CS17 Army ROCKS"
    ```

12. `cowsay` reads its input the same way `grep` and `wc` do, so it can be the last stage of a pipeline. Make the cow say how many things are in `gallery`. Use `ls`, `wc -l` and `cowsay`, joined with two `|`.

13. A cow is text like any other text, so it can go into a file. Send the cow to the end of `tidy-up-log.txt` instead of the screen, then show the file. Your name line from task 5 must still be at the top.

**One more prediction round.** Write your answer first. Then run the line and compare it with your answer.

| Command | Write your prediction, then run the line |
|---|---|
| `cat logs/*.txt \| wc -l` |  |
| `grep present club-members-attendance-register.txt \| wc -l` |  |
| `grep absent club-members-attendance-register.txt \| wc -l` |  |
| `cat documents/reports/*.txt \| grep budget \| wc -l` |  |
| `ls gallery \| wc -l` |  |

> **Remember**
>
> Read a pipeline from left to right, like a sentence: *show the logs, keep the failures, count them*. If a long pipeline gives a strange result, remove the last stage and run it again. This shows you what passes through the middle.

## Part 7. Save your history and hand in

*Lesson 4*

Everything that you typed in this assignment is still in the shell's history, and `history` prints it. A printed list is no use to anybody, so you send it into a file instead, with the `>` from Part 6. That file is what you hand in with the archive: it is the record of how you tidied it, in your own commands. Do this part last, in the same terminal window that you have used all along.

| Command | What it does |
|---|---|
| `history` | print every command that you ran in this window |
| `history > file` | put that list into a file instead of on the screen |
| `head -20 file` | show the first 20 lines of a file |
| `tail -20 file` | show the last 20 lines of a file |
| `mv a b c folder/` | move several files into a folder with one command |
| `zip -r name.zip folder` | pack a folder and everything inside it |

1. Start in the archive folder and check it with `pwd`. Print your command history one more time. It is long now, so show only the last twenty lines. Use `history`, a `|` and `tail`.

2. Save the whole history into a file with the name `history.txt`, in the archive folder. Nothing must appear on the screen. Then count the lines in the file.

3. Show the first ten lines of `history.txt`. Which command from Part 1 is at the top?

4. How many folders did you make in this whole assignment? Answer it from the file, with one command: search `history.txt` for `mkdir` and count the matching lines.

5. Make a folder with the name `submission` inside `cs17-archive`.

6. Move `gallery-list.txt`, `aisha-count.txt` and `tidy-up-log.txt` into it. Use one command for all three files. Leave `history.txt` in the archive folder.

7. Write your full name into `submission/name.txt`. Use one command.

8. List `submission` with the long details. Check that four files are there and that none of them is empty.

> **Remember**
>
> `history` belongs to the terminal window that you are in. Close the window before you save the file and the list starts again from nothing. Save `history.txt` before you close anything, and if you did lose it, say so when you hand in rather than typing a fake list: a short honest history is worth more than an invented one.

## Hand in

Part 7 built your hand-in. This is the last thing you do, and it is two commands. Go up one folder, to `terminal-assignment`, and pack the whole `cs17-archive` folder into a zip file with your own name in the filename. `zip` is the partner of `unzip`, and `-r` tells it to include every folder inside:

`cd ~/Desktop/terminal-assignment`

`zip -r submission-your-name.zip cs17-archive`

Upload that zip file. Hand in this sheet with it.

> **Check this list before you pack the zip.** Every line is something you can check with `ls`.
>
> - `gallery` holds the six camera photographs and the `competition-2026` folder, and the screenshot is gone.
> - `gallery/competition-2026` holds the three competition entries.
> - `backup` holds all four experiment logs, and `logs` still holds them too.
> - `sorted/notes` holds `last-year-notes.txt`, the copy of the Term 2 report and `camera-settings-backup.txt`.
> - Four folders that came in the zip are gone: `documents/drafts`, `documents/temp`, `inbox/old-phone-photos` and `inbox/Unsorted Camera Dump`.
> - `history.txt` is in `cs17-archive` itself, not in `submission`, and it is not empty.
> - `submission` holds four files. One of them has your name.
> - Every question, the map you copied in Part 1 and every table has an answer.

## Command reference

| Command | Use |
|---|---|
| `pwd` | show the folder that you are in |
| `ls` | list the contents of this folder |
| `ls -l` | list with the sizes and the dates |
| `ls -a` | list the hidden entries too |
| `cd` | change folder |
| `mkdir` | make a folder |
| `mkdir -p` | make every folder in the path that is missing |
| `touch` | make an empty file |
| `cat` | show the contents of a file |
| `cp` | copy a file |
| `mv` | move a file, or rename it |
| `rm` | delete a file. This is permanent |
| `rmdir` | delete an empty folder |
| `rmdir -p` | delete a folder and its parents, while each one is empty |
| `echo` | show text on the screen |
| `clear` | clear the screen |
| `history` | show the commands that you ran in this window |
| `head -n` | show the first n lines of a file |
| `tail -n` | show the last n lines of a file |
| `cowsay` | draw a cow saying something. It reads a pipe too |
| `grep` | show the lines of a file that contain a word |
| `wc` | count the lines, words and bytes |
| `wc -l` | count the lines only |
| `unzip` | unpack a zip file |
| `zip -r` | pack a folder and everything inside it into a zip file |
| `man` | open the manual of a command. Press q to quit |
| `--help` | ask a command to list its options |
| `>` | write output into a file and replace the contents |
| `>>` | add output to the end of a file |
| `\|` | send the output of one command into another command |
| `*` | match any text here |
| `..` | the folder above this one |
| `~` | your home folder |
| `"name with spaces"` | one name, not several arguments |
| `Tab` | finish the name that I started to type |
| `Up / Down` | move through the commands that you ran |
