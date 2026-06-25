<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <simulation>
    <title>RPL-ClusterIDS campaign (3 nodes, seed=1)</title>
    <randomseed>1</randomseed>
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
      <description>RPL-ClusterIDS Node</description>
      <source>[CONTIKI_DIR]/examples/IDS_IOT/code_source_RPL_ClusterIDS/clusterids-node.c</source>
      <commands>true</commands>
      <firmware>/home/madani/contiki-ng/examples/IDS_IOT/code_source_RPL_ClusterIDS/simulations/../build_cache/clusterids-node-MAIN.cooja</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Battery</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiRadio</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiClock</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiRS232</moteinterface>
      <moteinterface>org.contikios.cooja.contikimote.interfaces.ContikiLED</moteinterface>
    </motetype>

    <mote>
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>100.0</x>
        <y>100.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.contikimote.interfaces.ContikiMoteID
        <id>1</id>
      </interface_config>
      <motetype_identifier>mtype1</motetype_identifier>
    </mote>
    <mote>
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>100.0</x>
        <y>150.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.contikimote.interfaces.ContikiMoteID
        <id>2</id>
      </interface_config>
      <motetype_identifier>mtype1</motetype_identifier>
    </mote>
    <mote>
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>100.0</x>
        <y>200.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.contikimote.interfaces.ContikiMoteID
        <id>3</id>
      </interface_config>
      <motetype_identifier>mtype1</motetype_identifier>
    </mote>
  </simulation>

  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <script><![CDATA[
        TIMEOUT(120000, log.testOK());
var logfile = "/home/madani/contiki-ng/examples/IDS_IOT/code_source_RPL_ClusterIDS/simulations/logs/ids_campaign/log_MAIN_grid_3nodes_none_seed1.log";
while(true) {
  YIELD();
  if(typeof msg === "string" && msg.indexOf("METRIC,") === 0) {
    log.append(logfile, msg + "\n");
  }
}
      ]]></script>
      <active>true</active>
    </plugin_config>
    <width>500</width>
    <z>0</z>
    <height>300</height>
    <location_x>10</location_x>
    <location_y>10</location_y>
  </plugin>
</simconf>