import platform, subprocess

MAC = 'Darwin'
WINDOWS = 'Windows'
CPUINFO_FILE = '/proc/cpuinfo'


class Platform:
    def __init__(self):
        self.platform = platform.system()
        self.version = platform.version()
        self.release = platform.release()
        self.python_version = platform.python_version()

        try:
            self.cpuinfo = [i.strip() for i in open(CPUINFO_FILE)]
        except:
            self.cpuinfo = []

        def is_rpi_line(i):
            return i.startswith('Hardware') and i.endswith('BCM2708')

        self.is_raspberry_pi = any(is_rpi_line(i) for i in self.cpuinfo)
        self.is_linux = (self.platform == 'linux')

        platform_version = ()
        if self.is_linux:
            # Use the linux distribution as the name
            self.platform = platform.linux_distribution()[0].lower()
        elif self.platform == WINDOWS:
            platform_version = platform.win32_ver()
        elif self.platform == MAC:
            release, versioninfo, machine = platform.mac_ver()
            platform_version = release, machine
            # https://boklee.blogspot.com/2012/05/how-to-retrieve-cpuinfo-on-os-x.html
            for i in 'features', 'brand_string':
                s = subprocess.check_output(('sysctl', 'machdep.cpu.' + i))
                self.cpuinfo.append(s.decode().strip())

        self.platform_version = ':'.join(platform_version)
