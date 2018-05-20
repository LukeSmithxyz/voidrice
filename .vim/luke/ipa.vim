let g:IPAOn=0

function! ToggleIPA()
	if !g:IPAOn
		call IPA()
	else
		cal IPAOff()
	endif
endfunction

function! IPA()
	echo "IPA macros activated"
	let g:IPAOn=1
	imap ;nn ɲ̊
	imap ;gn ɲ
	imap ;ng ŋ
	imap ;' ʔ
	imap ;sh ʃ
	imap ;zh ʒ
	imap ;xi ɕ
	imap ;zi ʑ
	imap ;ph ɸ
	imap ;bh β
	imap ;th θ
	imap ;dh ð
	imap ;cc ç
	imap ;jj ʝ
	imap ;gh ɣ
	imap ;xx χ
	imap ;fr ʁ
	imap ;HH ħ
	imap ;hh ɦ
	imap ;vv ʋ
	imap ;er ɹ
	imap ;fl ɾ
	imap ;bb ʙ
	imap ;ih ɨ
	imap ;ii ɪ
	imap ;eu ɯ̽
	imap ;uu ʊ
	imap ;uh ə
	imap ;eh ɛ
	imap ;oe œ
	imap ;au ɔ
	imap ;ae æ
	imap ;aa ɐ
	imap ;OE ɶ
	imap ;ah ɑ
	imap ;ba ɒ
endfunction

function! IPAOff()
	echo "IPA macros off."
	let g:IPAOn=0
	iunmap ;nn
	iunmap ;gn
	iunmap ;ng
	iunmap ;'
	iunmap ;sh
	iunmap ;zh
	iunmap ;xi
	iunmap ;zi
	iunmap ;ph
	iunmap ;bh
	iunmap ;th
	iunmap ;dh
	iunmap ;cc
	iunmap ;jj
	iunmap ;gh
	iunmap ;xx
	iunmap ;fr
	iunmap ;HH
	iunmap ;hh
	iunmap ;vv
	iunmap ;er
	iunmap ;fl
	iunmap ;bb
	iunmap ;ih
	iunmap ;ii
	iunmap ;eu
	iunmap ;uu
	iunmap ;uh
	iunmap ;eh
	iunmap ;oe
	iunmap ;au
	iunmap ;ae
	iunmap ;aa
	iunmap ;OE
	iunmap ;ah
	iunmap ;ba
endfunction

" As of yet unimplemented:
"b̪
"t̼
"d̼
"ʈ
"ɖ
"ɟ
"ɡ
"ɢ
"ʡ
"ʂ
"ʐ
"θ̼
"ð̼
"θ̠
"ð̠
"ɹ̠̊
"ɹ̠
"ɻ
"ʕ
"ʢ
"ʋ̥
"ɹ̥
"ɻ̊
"ɻ
"j̊
"ɰ̊
"ɰ
"ʔ̞
"ⱱ̟
"ⱱ
"ɾ̼
"ɾ̥
"ɽ̊
"ɽ
"ɢ̆
"ʡ̮
"ʙ̥
"r̼
"r̥
"ɽ̊
"ɽ
"ʀ̥
"ʀ
"ʜ
"ʢ
"ɬ
"ɮ
"ɭ̊
"ʎ̥
"ʎ̝
"ʟ̝̊
"ʟ̝
"l̥
"ɭ̊
"ɭ
"ʎ̥
"ʎ
"ʟ̥
"ʟ
"ʟ̠
"ɺ
"ɺ̢
"ʎ̮
"ʟ̆
"ʉ
"ɯ
"ʏ
"ɪ̈
"ʊ̈
"ø
"ɘ
"ɵ
"ɤ
"e̞
"ø̞
"ɵ̞
"ɤ̞
"o̞
"ɜ
"ɞ
"ʌ
"ɞ̞
"ä
"ɒ̈
"m̥
"ɱ
"n̼
"n̥
"ɳ̊
"ɳ
"ŋ̊
"ɴ
"p̪
