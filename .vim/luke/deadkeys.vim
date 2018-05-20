
" Installation
" Source the file wherever you put it:
"	so ~/.vim/luke/deadkeys.vim
" Map ToggleDeadKeys to whatever you want:
"	nm <F7> :call ToggleDeadKeys()<CR>

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

	" under dot
	imap .D Ḍ
	imap .d ḍ
	imap .H Ḥ
	imap .h ḥ
	imap .L Ḹ
	imap .l ḹ
	imap .M Ṃ
	imap .m ṃ
	imap .N Ṇ
	imap .n ṇ
	imap .R Ṛ
	imap .r ṛ
	imap .G Ṝ
	imap .g ṝ
	imap .S Ṣ
	imap .s ṣ
	imap .T Ṭ
	imap .t ṭ

	" tilde
	imap ~a ã
	imap ~A Ã
	imap ~e ẽ
	imap ~E Ẽ
	imap ~i ĩ
	imap ~I Ĩ
	imap ~o õ
	imap ~O Õ
	imap ~u ũ
	imap ~U Ũ
	imap ~n ñ
	imap ~N Ñ

	" caron
	imap >A Ǎ
	imap >a ǎ
	imap >C Č
	imap >c č
	imap >E Ě
	imap >e ě
	imap >G Ǧ
	imap >g ǧ
	imap >I Ǐ
	imap >i ǐ
	imap >O Ǒ
	imap >o ǒ
	imap >R Ř
	imap >r ř
	imap >S Ṧ
	imap >s ṧ
	imap >U Ǔ
	imap >u ǔ
	imap >V Ǚ
	imap >v ǚ
	imap >Z Ž
	imap >z ž

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
	" under dot
	iunmap .D
	iunmap .d
	iunmap .H
	iunmap .h
	iunmap .L
	iunmap .l
	iunmap .M
	iunmap .m
	iunmap .N
	iunmap .n
	iunmap .R
	iunmap .r
	iunmap .G
	iunmap .g
	iunmap .S
	iunmap .s
	iunmap .T
	iunmap .t

	"tilde
	iunmap ~a
	iunmap ~A
	iunmap ~e
	iunmap ~E
	iunmap ~i
	iunmap ~I
	iunmap ~o
	iunmap ~O
	iunmap ~u
	iunmap ~U
	iunmap ~n

	" caron
	iunmap >A
	iunmap >a
	iunmap >C
	iunmap >c
	iunmap >E
	iunmap >e
	iunmap >G
	iunmap >g
	iunmap >I
	iunmap >i
	iunmap >O
	iunmap >o
	iunmap >R
	iunmap >r
	iunmap >S
	iunmap >s
	iunmap >U
	iunmap >u
	iunmap >V
	iunmap >v
	iunmap >Z
	iunmap >z

endfunction
