#!/usr/bin/env python3
"""Generate a headless-ready Cooja .csc for IDS campaign simulations."""
from __future__ import annotations

import argparse
from pathlib import Path


def grid_positions(n: int, spacing: int = 50) -> list[tuple[int, int]]:
    cols = max(1, int(n ** 0.5))
    pos = []
    for i in range(n):
        x = (i % cols) * spacing + 100
        y = (i // cols) * spacing + 100
        pos.append((x, y))
    return pos


def make_mote_blocks(positions: list[tuple[int, int]]) -> str:
    blocks = []
    for i, (x, y) in enumerate(positions, start=1):
        blocks.append(f"""\
    <mote>
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>{x}.0</x>
        <y>{y}.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.contikimote.interfaces.ContikiMoteID
        <id>{i}</id>
      </interface_config>
    </mote>""")
    return "\n".join(blocks)


def generate_csc(
    nodes: int,
    seed: int,
    variant: str,
    log_path: str,
    timeout_ms: int,
    scenario: str = "none",
) -> str:
    positions = grid_positions(nodes)
    motes_xml = make_mote_blocks(positions)

    js_script = (
        'TIMEOUT(%d, log.testOK());\n'
        'var logfile = "%s";\n'
        'while(true) {\n'
        '  YIELD();\n'
        '  if(typeof msg === "string" && msg.indexOf("METRIC,") === 0) {\n'
        '    log.append(logfile, msg + "\\n");\n'
        '  }\n'
        '}'
    ) % (timeout_ms, log_path)

    make_cmds = (
        '$(MAKE) -j$(CPUS) clusterids-node.cooja TARGET=cooja '
        f'IDS_VARIANT={variant} IDS_CONF_CAMPAIGN_METRICS=1'
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <simulation>
    <title>RPL-ClusterIDS campaign ({variant}, {scenario}, {nodes} nodes, seed={seed})</title>
    <randomseed>{seed}</randomseed>
    <motedelay_us>1000000</motedelay_us>

    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>1.0</success_ratio_rx>
    </radiomedium>

    <events>
      <logoutput>40000</logoutput>
    </events>

    <motetype>
      org.contikios.cooja.contikimote.ContikiMoteType
      <identifier>mtype1</identifier>
      <description>RPL-ClusterIDS Node ({variant})</description>
      <source>[CONTIKI_DIR]/examples/IDS_IOT/code_source_RPL_ClusterIDS/clusterids-node.c</source>
      <commands>{make_cmds}</commands>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Battery</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiRadio</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiClock</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiRS232</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiLED</moteinterface>
{motes_xml}
    </motetype>
  </simulation>

  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <script><![CDATA[
        {js_script}
      ]]></script>
      <active>true</active>
    </plugin_config>
    <width>500</width>
    <z>0</z>
    <height>300</height>
    <location_x>10</location_x>
    <location_y>10</location_y>
  </plugin>
</simconf>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes", type=int, default=50, help="Number of sensor nodes")
    ap.add_argument("--seed", type=int, default=1001, help="Random seed (default: 1001 per seeds.txt)")
    ap.add_argument("--variant", type=str, default="MAIN",
                    choices=["MAIN", "B1", "B2", "B3", "MAIN_NOCLUS", "MAIN_NOML", "MAIN_NOCTX", "MAIN_NOENR"],
                    help="IDS variant")
    ap.add_argument("--scenario", type=str, default="none", help="Attack scenario identifier")
    ap.add_argument("--log", type=str, default="", help="Path for METRIC log output")
    ap.add_argument("--timeout-ms", type=int, default=10800000, help="Simulation timeout in ms")
    ap.add_argument("--out", type=Path, required=True, help="Output .csc file path")
    ap.add_argument("--topology", type=str, default="grid", choices=["grid", "random"], help="Topology type")
    args = ap.parse_args()

    log_path = str(Path(args.log).resolve()) if args.log else str(args.out.with_suffix(".log").resolve())

    csc = generate_csc(
        nodes=args.nodes,
        seed=args.seed,
        variant=args.variant,
        log_path=log_path,
        timeout_ms=args.timeout_ms,
        scenario=args.scenario,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(csc, encoding="utf-8")
    print(f"Wrote {args.out} ({args.nodes} motes, seed={args.seed}, timeout={args.timeout_ms}ms)")


if __name__ == "__main__":
    main()
