#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
# Copyright (c) 2023 KylinSoft  Co., Ltd. All Rights Reserved.

import time
from common.config import Config
from kyreport.ky_data_collection import DATACOLLECTION

class KyReport:

    def ky_build(self, work, inst, tm):
        curr_time = time.strftime("%m%d%H%M")
        srcfile   = Config.get_inst_path()   + 'kyreport/extuner_report.html'
        outfile   = Config.get_output_path() + 'extuner_report_' + curr_time + '.html'
        info      = {
                'tm_info'  : { 'start': '', 'stop': '' },
                'base_info': {
                    'hostname'      : '',
                    'system_version': '',
                    'kernel_version': '',
                    'gcc_version'   : '',
                    'glibc_version' : '',
                    'jdk_version'   : '',
                    'net_sum'       : [],
                    'disk_sum'      : [],
                    'cpu_model'     : '',
                    'cpu_arch'      : '',
                    'cpu_cores'     : '',
                    'mem_total'     : '',
                    'mem_free'      : '',
                    'mem_available' : ''
                },
                'cpu_info' : [],
                'mem_info' : [],
                'net_info' : [],
                'io_info'  : [],
                'synthesis_info'  : [],
                'jvm_info' : [],
                'sys_param': [],
                'sys_msg'  : [],
                'hotspot_info': [],
            }

        # setting timer info
        info['tm_info']['start'] = tm['start']
        info['tm_info']['stop']  = tm['stop']
        # end timer info

        # setting base info
        info['base_info']['hostname']         = Command.cmd_exec(r'hostname')
        info['base_info']['system_version']   = Command.cmd_exec(r'cat /etc/.productinfo | grep release')
        info['base_info']['kernel_version']   = Command.cmd_exec(r'uname -r')
        info['base_info']['gcc_version']      = Command.cmd_exec(r'gcc --version | head -n 1')
        # end base info

        # setting base cpu info
        info['base_info']['cpu_model']        = Command.cmd_exec('export LANG="en_US.UTF-8" && lscpu | grep \'Model name:\' | cut -d \':\' -f 2 | sed -e \'s/^[ ]*//g\' | sed -e \'s/[ ]*$//g\'')
        info['base_info']['cpu_arch']         = Command.cmd_exec('export LANG="en_US.UTF-8" && lscpu | grep \'Architecture:\' | cut -d \':\' -f 2 | sed -e \'s/^[ ]*//g\' | sed -e \'s/[ ]*$//g\'')
        info['base_info']['cpu_cores']        = Command.cmd_exec('export LANG="en_US.UTF-8" && lscpu | grep \'CPU(s)\' | grep -v -E "NUMA|On-line" | cut -d \':\' -f 2 | sed -e \'s/^[ ]*//g\' | sed -e \'s/[ ]*$//g\'')
        # end base cpu info

        # setting base mem info
        info['base_info']['mem_total']        = Command.cmd_exec('cat /proc/meminfo | grep "MemTotal" | cut -d \':\' -f 2 | sed -e "s/^[ ]*//g" | cut -d \' \' -f 1')
        info['base_info']['mem_free']         = Command.cmd_exec('cat /proc/meminfo | grep "MemFree" | cut -d \':\' -f 2 | sed -e "s/^[ ]*//g" | cut -d \' \' -f 1')
        info['base_info']['mem_available']    = Command.cmd_exec('cat /proc/meminfo | grep "MemAvailable" | cut -d \':\' -f 2 | sed -e "s/^[ ]*//g" | cut -d \' \' -f 1')
        # end base mem info
        
        # setting menu info
        if os.path.exists(Config.get_output_path() + 'CPUInfo.txt'):
            info['cpu_info']  = DATACOLLECTION().get_cpu_tag_data()
        if os.path.exists(Config.get_output_path() + 'memInfo.txt'):
            info['mem_info']  = self.build_info(Config.get_output_path() + 'memInfo.txt')
        if os.path.exists(Config.get_output_path() + 'netInfo.txt'):
            info['net_info']  = self.build_info(Config.get_output_path() + 'netInfo.txt')
        if os.path.exists(Config.get_output_path() + 'diskInfo.txt'):
            info['io_info']   = self.build_info(Config.get_output_path() + 'diskInfo.txt')
        if os.path.exists(Config.get_output_path() + 'CPUInfo.txt'):
            info['synthesis_info']   = DATACOLLECTION().get_synthesis_tag_data()
        if os.path.exists(Config.get_output_path() + 'sysParamInfo.txt'):
            info['sys_param'] = self.build_info(Config.get_output_path() + 'sysParamInfo.txt')
        if os.path.exists(Config.get_output_path() + 'systemMessage.txt'):
            info['sys_msg']   = self.build_info(Config.get_output_path() + 'systemMessage.txt')
        if os.path.exists(Config.get_output_path() + 'hotspotInfo.txt'):
            if os.path.getsize(Config.get_output_path() + 'hotspotInfo.txt'):
                info['hotspot_info'] = self.build_info(Config.get_output_path() + 'hotspotInfo.txt')
        
        info['common_cmd']['pidstatinfo'] = GlobalParameter().pidstat_cmd
        info['common_cmd']['subsarinfo'] = GlobalParameter().sub_sarall
        # ending menu info

        content  = """
<script type="text/javascript">
var info = %s

window.onload = init();
</script>
"""%(json5.dumps(info))
 shutil.copyfile(srcfile, outfile)
        fp = open(outfile, 'a')
        fp.write(content)
        fp.close()
        # Logger().info('Report file generated success: {}'.format(outfile))
        Logger().info(u'采集报告输出路径: {}'.format(outfile))

    @staticmethod
    def build_netsum():
        net_list = []
        str_comm = 'ethtool -i '
        ifc_text = Command.cmd_exec('nmcli device status | awk \'{i++; if(i>1 && "--"!=$4) {print $1}}\'')
        ifc_name = ifc_text.split('\n', -1)
        for ifc in ifc_name:
            if 0 != len(ifc.strip()) and  '--' != ifc:
                net_obj = { 'name': '', 'driver': '', 'version': '', 'firmware_version': '', 'link_status': '' }
                net_obj['name']             = ifc
                net_obj['driver']           = Command.cmd_exec(str_comm + ifc + ' | grep driver | cut -d \' \' -f 2')
                net_obj['version']          = Command.cmd_exec(str_comm + ifc + ' | grep version | grep -v -E \'firmware-version|expansion-rom-version\' | cut -d \' \' -f 2')
                net_obj['firmware_version'] = Command.cmd_exec(str_comm + ifc + ' | grep firmware-version | cut -d \' \' -f 2')
                net_obj['link_status']      = Command.cmd_exec('ethtool ' + ifc + ' | grep \'Link detected\' | cut -d \' \' -f 3')
                net_obj['addr']             = Command.cmd_exec('ifconfig ' + ifc + ' | grep "inet " | awk \'{print $2}\' ').strip()
                 net_obj['netmask']          = Command.cmd_exec('ifconfig ' + ifc + ' | grep "inet " | awk \'{print $4}\' ').strip()
                net_list.append(net_obj)

        return net_list
