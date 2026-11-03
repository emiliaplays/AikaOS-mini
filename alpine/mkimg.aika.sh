profile_aika() {
    profile_standard
    title="AikaOS Mini 11.1"
    desc="AikaOS Mini Live CD with IceWM and Firefox ESR"
    image_name="aikaos-mini"
    hostname="aika-mini"
    kernel_addons=""
    boot_addons="amd-ucode intel-ucode"
    initrd_ucode="/boot/amd-ucode.img /boot/intel-ucode.img"
    kernel_cmdline="console=ttyS0,115200 console=tty0"
    syslinux_serial="0 115200"
    apks="$(cat /aika/world)"
    apkovl="genapkovl-aika.sh"
}
