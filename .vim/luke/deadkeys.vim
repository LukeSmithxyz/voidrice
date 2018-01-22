let g:DeadKeysOn=0

function! ToggleDeadKeys()
	if !g:DeadKeysOn
		call DeadKeys()
	else
		call DeadKeysOff()
	endif
endfunction

function! DeadKeys()
	echo "Dead Keys: On"
	let g:DeadKeysOn=1
	" grave accents
	imap `a à
	imap `e è
	imap `i ì
	imap `o ò
	imap `u ù
	imap `A À
	imap `E È
	imap `I Ì
	imap `O Ò
	imap `U Ù
	imap `<space> `

	" umlaut
	imap "a ä
	imap "e ë
	imap "i ï
	imap "o ö
	imap "u ü
	imap "A Ä
	imap "E Ë
	imap "I Ï
	imap "O Ö
	imap "U Ü
	imap "<space> "

	" macrons
	imap :a ā
	imap :e ē
	imap :i ī
	imap :o ō
	imap :u ū
	imap :A Ā
	imap :E Ē
	imap :I Ī
	imap :O Ō
	imap :U Ū

	" acute accents
	imap 'a á
	imap 'A Á
	imap 'C Ć
	imap 'c ć
	imap 'e é
	imap 'E É
	imap 'i í
	imap 'I Í
	imap 'N Ń
	imap 'n ń
	imap 'o ó
	imap 'R Ŕ
	imap 'r ŕ
	imap 'S Ś
	imap 's ś
	imap 'O Ó
	imap 'u ú
	imap 'U Ú
	imap '<space> '
endfunction "deadkeys()

function! DeadKeysOff()
	echo "Dead Keys: Off"
	let g:DeadKeysOn=0

	" unmapping graves
	iunmap `a
	iunmap `e
	iunmap `i
	iunmap `o
	iunmap `u
	iunmap `A
	iunmap `E
	iunmap `I
	iunmap `O
	iunmap `U
	iunmap `<space>

	" unmapping umlauts
	iunmap "a
	iunmap "e
	iunmap "i
	iunmap "o
	iunmap "u
	iunmap "A
	iunmap "E
	iunmap "I
	iunmap "O
	iunmap "U
	iunmap "<space>

	" unmapping macrons
	iunmap :a
	iunmap :e
	iunmap :i
	iunmap :o
	iunmap :u
	iunmap :A
	iunmap :E
	iunmap :I
	iunmap :O
	iunmap :U

	" unmapping acutes
	iunmap 'a
	iunmap 'A
	iunmap 'C
	iunmap 'c
	iunmap 'e
	iunmap 'E
	iunmap 'i
	iunmap 'I
	iunmap 'N
	iunmap 'n
	iunmap 'o
	iunmap 'R
	iunmap 'r
	iunmap 'S
	iunmap 's
	iunmap 'O
	iunmap 'u
	iunmap 'U
	iunmap '<space>
endfunction
