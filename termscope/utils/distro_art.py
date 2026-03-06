from __future__ import annotations

import re

from rich.text import Text

TOKEN_RE = re.compile(r"(\$\{c[1-6]\})")

DEFAULT_ART_RAW = r'''
${c1}      .--.
${c1}     |o_o |
${c1}     |:_/ |
${c1}    //   \ \
${c1}   (|     | )
${c1}  /'\_   _/`\\
${c1}  \___)=(___/
'''.strip("\n")

DISTRO_ART_RAW_MAP: dict[str, str] = {
    "arch": r'''
${c1}                   -`
${c1}                  .o+`
${c1}                 `ooo/
${c1}                `+oooo:
${c1}               `+oooooo:
${c1}               -+oooooo+:
${c1}             `/:-:++oooo+:
${c1}            `/++++/+++++++:
${c1}           `/++++++++++++++:
${c1}          `/+++o${c2}oooooooo${c1}oooo/`
${c2}         ${c1}./${c2}ooosssso++osssssso${c1}+`
${c2}        .oossssso-````/ossssss+`
${c1}       -osssssso.      :ssssssso.
${c1}      :osssssss/        osssso+++.
${c1}     /ossssssss/        +ssssooo/-
${c1}   `/ossssso+/:-        -:/+osssso+-
${c1}  `+sso+:-`                 `.-/+oso:
${c1} `++:.                           `-/+/
${c1} .`                                 `/
'''.strip("\n"),
    "cachyos": r'''
${c3}           ${c2}.${c3}-------------------------:
${c3}          .${c1}+=${c3}========================.
${c3}         :${c1}++${c3}===${c1}++===${c3}===============-       :${c1}++${c3}-
${c3}        :${c1}*++${c3}====${c1}+++++==${c3}===========-        .==:
${c3}       -${c1}*+++${c3}=====${c1}+***++=${c3}=========:
${c3}      =${c1}*++++=${c3}=======------------:
${c3}     =${c1}*+++++=${c3}====-                     ${c2}...${c3}
${c3}   .${c1}+*+++++${c3}=-===:                    .${c1}=+++=${c3}:
${c3}  :${c1}++++${c3}=====-==:                     -***${c1}**${c3}+
${c3} :${c1}++=${c3}=======-=.                      .=+**+${c2}.${c3}
${c3}.${c1}+${c3}==========-.                          ${c2}.${c3}
${c3} :${c1}+++++++${c3}====-                                ${c2}.${c3}--==-${c2}.${c3}
${c3}  :${c1}++${c3}==========.                             ${c2}:${c1}+++++++${c3}${c2}:
${c3}   .-===========.                            =*****+*+
${c3}    .-===========:                           .+*****+:
${c3}      -=======${c1}++++${c3}:::::::::::::::::::::::::-:  ${c2}.${c3}---:
${c3}       :======${c1}++++${c3}====${c1}+++******************=.
${c3}        :=====${c1}+++${c3}==========${c1}++++++++++++++*-
${c3}         .====${c1}++${c3}==============${c1}++++++++++*-
${c3}          .===${c1}+${c3}==================${c1}+++++++:
${c3}           .-=======================${c1}+++:
${c3}             ${c2}..........................
'''.strip("\n"),
    "ubuntu": r'''
${c1}            .-/+oossssoo+\-.
${c1}        ´:+ssssssssssssssssss+:`
${c1}      -+ssssssssssssssssssyyssss+-
${c1}    .ossssssssssssssssss${c2}dMMMNy${c1}sssso.
${c1}   /sssssssssss${c2}hdmmNNmmyNMMMMh${c1}ssssss\
${c1}  +sssssssss${c2}hm${c1}yd${c2}MMMMMMMNddddy${c1}ssssssss+
${c1} /ssssssss${c2}hNMMM${c1}yh${c2}hyyyyhmNMMMNh${c1}ssssssss\
${c1}.ssssssss${c2}dMMMNh${c1}ssssssssss${c2}hNMMMd${c1}ssssssss.
${c1}+ssss${c2}hhhyNMMNy${c1}ssssssssssss${c2}yNMMMy${c1}sssssss+
${c1}oss${c2}yNMMMNyMMh${c1}ssssssssssssss${c2}hmmmh${c1}ssssssso
${c1}oss${c2}yNMMMNyMMh${c1}sssssssssssssshmmmh${c1}ssssssso
${c1}+ssss${c2}hhhyNMMNy${c1}ssssssssssss${c2}yNMMMy${c1}sssssss+
${c1}.ssssssss${c2}dMMMNh${c1}ssssssssss${c2}hNMMMd${c1}ssssssss.
${c1} \ssssssss${c2}hNMMM${c1}yh${c2}hyyyyhdNMMMNh${c1}ssssssss/
${c1}  +sssssssss${c2}dm${c1}yd${c2}MMMMMMMMddddy${c1}ssssssss+
${c1}   \sssssssssss${c2}hdmNNNNmyNMMMMh${c1}ssssss/
${c1}    .ossssssssssssssssss${c2}dMMMNy${c1}sssso.
${c1}      -+sssssssssssssssss${c2}yyy${c1}ssss+-
${c1}        `:+ssssssssssssssssss+:`
${c1}            .-\+oossssoo+/-.
'''.strip("\n"),
    "debian": r'''
${c2}       _,met$$$$$gg.
${c2}    ,g$$$$$$$$$$$$$$$P.
${c2}  ,g$$P"        """Y$$.".
${c2} ,$$P'              `$$$.
${c2}',$$P       ,ggs.     `$$b:
${c2}`d$$'     ,$P"'   ${c1}.${c2}    $$$
${c2} $$P      d$'     ${c1},${c2}    $$P
${c2} $$:      $$.   ${c1}-${c2}    ,d$$'
${c2} $$;      Y$b._   _,d$P'
${c2} Y$$.    ${c1}`.${c2}`"Y$$$$P"'
${c2} `$$b      ${c1}"-.__
${c2}  `Y$$
${c2}   `Y$$.
${c2}     `$$b.
${c2}       `Y$$b.
${c2}          `"Y$b._
${c2}              `"""
'''.strip("\n"),
    "fedora": r'''
${c1}             .',;::::;,'.
${c1}         .';:cccccccccccc:;,.
${c1}      .;cccccccccccccccccccccc;.
${c1}    .:cccccccccccccccccccccccccc:.
${c1}  .;ccccccccccccc;${c2}.:dddl:.${c1};ccccccc;.
${c1} .:ccccccccccccc;${c2}OWMKOOXMWd${c1};ccccccc:.
${c1}.:ccccccccccccc;${c2}KMMc${c1};cc;${c2}xMMc${c1};ccccccc:.
${c1},cccccccccccccc;${c2}MMM.${c1};cc;${c2};WW:${c1};cccccccc,
${c1}:cccccccccccccc;${c2}MMM.${c1};cccccccccccccccc:
${c1}:ccccccc;${c2}oxOOOo${c1};${c2}MMM0OOk.${c1};cccccccccccc:
${c1}cccccc;${c2}0MMKxdd:${c1};${c2}MMMkddc.${c1};cccccccccccc;
${c1}ccccc;${c2}XM0'${c1};cccc;${c2}MMM.${c1};cccccccccccccccc'
${c1}ccccc;${c2}MMo${c1};ccccc;${c2}MMW.${c1};ccccccccccccccc;
${c1}ccccc;${c2}0MNc.${c1}ccc${c2}.xMMd${c1};ccccccccccccccc;
${c1}cccccc;${c2}dNMWXXXWM0:${c1};cccccccccccccc:,
${c1}cccccccc;${c2}.:odl:.${c1};cccccccccccccc:,.
${c1}:cccccccccccccccccccccccccccc:'.
${c1}.:cccccccccccccccccccccc:;,..
${c1}  '::cccccccccccccc::;,.
'''.strip("\n"),
    "nixos": r'''
${c1}          ▗▄▄▄       ${c2}▗▄▄▄▄    ▄▄▄▖
${c1}          ▜███▙       ${c2}▜███▙  ▟███▛
${c1}           ▜███▙       ${c2}▜███▙▟███▛
${c1}            ▜███▙       ${c2}▜██████▛
${c1}     ▟█████████████████▙ ${c2}▜████▛     ${c1}▟▙
${c1}    ▟███████████████████▙ ${c2}▜███▙    ${c1}▟██▙
${c2}           ▄▄▄▄▖           ▜███▙  ${c1}▟███▛
${c2}          ▟███▛             ▜██▛ ${c1}▟███▛
${c2}         ▟███▛               ▜▛ ${c1}▟███▛
${c2}▟███████████▛                  ${c1}▟██████████▙
${c2}▜██████████▛                  ${c1}▟███████████▛
${c2}      ▟███▛ ${c1}▟▙               ▟███▛
${c2}     ▟███▛ ${c1}▟██▙             ▟███▛
${c2}    ▟███▛  ${c1}▜███▙           ▝▀▀▀▀
${c2}    ▜██▛    ${c1}▜███▙ ${c2}▜██████████████████▛
${c2}     ▜▛     ${c1}▟████▙ ${c2}▜████████████████▛
${c1}           ▟██████▙       ${c2}▜███▙
${c1}          ▟███▛▜███▙       ${c2}▜███▙
${c1}         ▟███▛  ▜███▙       ${c2}▜███▙
${c1}         ▝▀▀▀    ▀▀▀▀▘       ${c2}▀▀▀▘
'''.strip("\n"),
    "gentoo": r'''
${c1}         -/oyddmdhs+:.
${c1}     -o${c2}dNMMMMMMMMNNmhy+${c1}-`
${c1}   -y${c2}NMMMMMMMMMMMNNNmmdhy${c1}+-
${c1} `o${c2}mMMMMMMMMMMMMNmdmmmmddhhy${c1}/`
${c1} om${c2}MMMMMMMMMMMN${c1}hhyyyo${c2}hmdddhhhd${c1}o`
${c1}.y${c2}dMMMMMMMMMMd${c1}hs++so/s${c2}mdddhhhhdm${c1}+`
${c1} oy${c2}hdmNMMMMMMMN${c1}dyooy${c2}dmddddhhhhyhN${c1}d.
${c1}  :o${c2}yhhdNNMMMMMMMNNNmmdddhhhhhyym${c1}Mh
${c1}    .:${c2}+sydNMMMMMNNNmmmdddhhhhhhmM${c1}my
${c1}       /m${c2}MMMMMMNNNmmmdddhhhhhmMNh${c1}s:
${c1}    `o${c2}NMMMMMMMNNNmmmddddhhdmMNhs${c1}+`
${c1}  `s${c2}NMMMMMMMMNNNmmmdddddmNMmhs${c1}/.
${c1} /N${c2}MMMMMMMMNNNNmmmdddmNMNdso${c1}:`
${c1}+M${c2}MMMMMMNNNNNmmmmdmNMNdso${c1}/-
${c1}yM${c2}MNNNNNNNmmmmmNNMmhs+/${c1}-`
${c1}/h${c2}MMNNNNNNNNMNdhs++/${c1}-`
${c1}`/${c2}ohdmmddhys+++/:${c1}.`
${c1}  `-//////:--.
'''.strip("\n"),
    "alpine": r'''
${c1}       .hddddddddddddddddddddddh.
${c1}      :dddddddddddddddddddddddddd:
${c1}     /dddddddddddddddddddddddddddd/
${c1}    +dddddddddddddddddddddddddddddd+
${c1}  `sdddddddddddddddddddddddddddddddds`
${c1} `ydddddddddddd++hdddddddddddddddddddy`
${c1}.hddddddddddd+`  `+ddddh:-sdddddddddddh.
${c1}hdddddddddd+`      `+y:    .sddddddddddh
${c1}ddddddddh+`   `//`   `.`     -sddddddddd
${c1}ddddddh+`   `/hddh/`   `:s-    -sddddddd
${c1}ddddh+`   `/+/dddddh/`   `+s-    -sddddd
${c1}ddd+`   `/o` :dddddddh/`   `oy-    .yddd
${c1}hdddyo+ohddyosdddddddddho+oydddy++ohdddh
${c1}.hddddddddddddddddddddddddddddddddddddh.
${c1} `yddddddddddddddddddddddddddddddddddy`
${c1}  `sdddddddddddddddddddddddddddddddds`
${c1}    +dddddddddddddddddddddddddddddd+
${c1}     /dddddddddddddddddddddddddddd/
${c1}      :dddddddddddddddddddddddddd:
${c1}       .hddddddddddddddddddddddh.
'''.strip("\n"),
}

DISTRO_ART_COLOR_MAP: dict[str, dict[str, str]] = {
    "default": {"${c1}": "bold #84a9d8", "${c2}": "bold #c5c8c6", "${c3}": "bold #8abeb7"},
    "arch": {"${c1}": "bold #8abeb7", "${c2}": "bold #c5c8c6"},
    "cachyos": {"${c1}": "bold #b5bd68", "${c2}": "bold #969896", "${c3}": "bold #8abeb7"},
    "ubuntu": {"${c1}": "bold #cc6666", "${c2}": "bold #c5c8c6"},
    "debian": {"${c1}": "bold #cc6666", "${c2}": "bold #ff6e9d"},
    "fedora": {"${c1}": "bold #81a2be", "${c2}": "bold #c5c8c6"},
    "nixos": {"${c1}": "bold #81a2be", "${c2}": "bold #8abeb7"},
    "gentoo": {"${c1}": "bold #b294bb", "${c2}": "bold #c5c8c6"},
    "alpine": {"${c1}": "bold #81a2be", "${c2}": "bold #b294bb", "${c3}": "bold #c5c8c6", "${c4}": "bold #8abeb7"},
}


def _raw_art(distro_id: str) -> str:
    return DISTRO_ART_RAW_MAP.get((distro_id or "").lower(), DEFAULT_ART_RAW)


def get_distro_art(distro_id: str) -> str:
    return TOKEN_RE.sub("", _raw_art(distro_id))


def get_distro_art_rich_lines(distro_id: str) -> list[Text]:
    raw = _raw_art(distro_id)
    color_map = DISTRO_ART_COLOR_MAP.get((distro_id or "").lower(), DISTRO_ART_COLOR_MAP["default"])
    lines: list[Text] = []

    for raw_line in raw.splitlines():
        line = Text()
        current_style = color_map.get("${c1}", DISTRO_ART_COLOR_MAP["default"]["${c1}"])
        for part in TOKEN_RE.split(raw_line):
            if not part:
                continue
            if TOKEN_RE.fullmatch(part):
                current_style = color_map.get(part, current_style)
            else:
                line.append(part, style=current_style)
        lines.append(line)

    return lines
