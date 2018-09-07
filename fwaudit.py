Firmware Audit, v0.0.4-PRE-ALPHA
This release is not yet feature complete, but is usable.
# Check file size against max buffer before opening/reading. Disallow large files until buffering logic added.
# After initial creation of dir, don't keep updating owner/group/file-mode each run, only do that once.
# Fix list/dict issues with get_tool_arg()/set_tool_arg(). Simplify by removing 'args' dict, and putting args one level higher.
# Test sidecar hash file format against sha256sum tool.
# Understand how to properly set single GID from list, especially macOS non-POSIX behavior. Test sudo use with a user account and/or a root account that has multiple group memberships, including >16.
# Test sidecar hash files and manifest using sha26sum
# Fix manifest, dealing with path names, not just same-directory filenames, in a manifest file, such that sha256sum tool can verify it, so they can be used at PRD level, not just PTD level.
# Standardize use of return codes, int -vs- bool, some overwrite,
#     raise LookupError('msg')
#     status = os.EX_(OK, USAGE, DATAERROR, NOINPUT, NOTFOUND, NOPERM)
# Standardize use of output formatting, esp in large output templates
#    form = '{0:0.3d} xxx {1:0.2f}'; print(form.format(d,f))
#    form = '''...{foo} ... {bar} ...'''; #print(form.format(foo='x', bar='y'))
# XXX add floating point
__version__ = '0.0.4'
__status__ = 'PRE-ALPH
    'full_name': 'Firmware Audit (fwaudit)',
    'max_profiles': '1000',
    'meta_profile': [],
    'hash_mode': True,  # --hash, --nohash
    'manifest_mode': True,  # --manifest, --nomanifest
    'max_buf': 50000,  # XXX add way to override. Proper value?
        'name': 'intel_amt_discovery',
        'tool': 'INTEL-SA-00075-Discovery-Tool',
        'desc': 'INTEL-SA-00075-Discovery-Tool',
        'mode': 'live',
        'exrc': 254,
        'expected': [],
        'actual': [],
        'args': {}
    }, {
        'name': 'intel_me_detection',
        'tool': 'intel_sa00086.py',
        'desc': 'INTEL-SA-00086-Detection-Tool',
        'mode': 'live',
        'exrc': 254,
        'expected': [],
        'actual': [],
        'args': {}
    }, {

        start_cpu = time.clock()
        start_real = time.time()
        end_cpu = time.clock()
        end_real = time.time()
        # XXX save this in per-run stats. Also create per-tool time stats elsewhere.
        cpu_seconds = end_cpu - start_cpu
        real_seconds = end_real - start_real
        debug('Total CPU seconds: ' + str(cpu_seconds))
        debug('Total Seconds: ' + str(real_seconds))
    epilog = 'For more information, please read the User Guide (README).'
                   help='Specify target directory to store generated files. Not compatible with sudo case, use as root or with su.')
                   help='Specify how to log tool output. Currently for root use only, do not use with sudo use.')
                   help='Generate manifest file of hashes for generated files.')
                   help='Generate SHA256 sidecar hash files for generated files.')
        APP_METADATA['version'])
    log(APP_METADATA['full_name'] + ' Version ' + APP_METADATA['version'])
# The critical code wraps message between "ERROR: " and "!", and displays more info on the exception e.
# Use critical() to display ERROR (fatal exceptions) messages.
def critical(e, msg):
    '''Simple critical wrapper to log()'''
    # e.message  # Python 2-only
    # e.__cause__ # Python 3-only
    # e.__context__  # Python 3-only
    # e.__traceback__ # Python 3-only
    # # IOError errno (d), strerror (s), filename (?)
    if e is not None:
        log('Exception ' + str(e.errno) + ': ' + str(e.message),
            prefix_fg_color=COLOR_DEFAULTS['error_pre_fg'],
            prefix_bg_color=COLOR_DEFAULTS['error_pre_bg'],
            msg_fg_color=COLOR_DEFAULTS['error_msg_fg'],
            msg_bg_color=COLOR_DEFAULTS['error_msg_bg'])
    if app_state['colorize']:
        log(msg, prefix='[ERROR] ', suffix='!',
            prefix_fg_color=COLOR_DEFAULTS['error_pre_fg'],
            prefix_bg_color=COLOR_DEFAULTS['error_pre_bg'],
            msg_fg_color=COLOR_DEFAULTS['error_msg_fg'],
            msg_bg_color=COLOR_DEFAULTS['error_msg_bg'])
    else:
        output(msg)


def return_hash_str_of_file(path):
    '''For a given file, return the sha256 hash string.
    
    Returns a SHA256 hash string if successful, None if unsuccessful.'''
    if is_none_or_null(path):
        error('Filename to hash unspecified')
        return None
    if not path_exists(path):
        error('File to hash does not exist: ' + path)
        return None
    debug('file to hash: ' + path)
    hash_str = None
    try:
        with open(path, 'rb') as f:
            buf = f.read()
            h = hashlib.sha256(buf)
            h.update(buf)
            hash_str = h.hexdigest()
            debug('hash: ' + hash_str)
    except OSError as e:
        critical(e, 'failed to hash file')
        hash_str = None
        sys.exc_info()
    return hash_str
def create_sidecar_hash_file(path):
    '''For a given file, create a 'side-car' hash file.
    
    Use a sha256sum-compatible file format, a single line consisting of:
        <hash> + <space> + <filename>
    XXX what newline format required?
    Future: Should support other formats, certutil.exe, etc. What formats?

    Returns True if successful, False if unsuccessful.'''
    if is_none_or_null(path):
        error('Filename to hash unspecified')
    if not path_exists(path):
        error('File to hash does not exist: ' + path)
    debug('path of file to hash: ' + path)
    base_filename = os.path.basename(path)
    if is_none_or_null(base_filename):
        error('Filename to hash unspecified')
    debug('base name of file to hash: ' + base_filename)
    hash_str = return_hash_str_of_file(path)
    if is_none_or_null(hash_str):
        error('Hash is empty')
    debug('hash of file: ' + hash_str)
    sidecar_path = path + '.sha256'
    if path_exists(sidecar_path):
        error('Sidecar hash file already exists, not overwriting')
        return False
    debug('sidecar filename: ' + sidecar_path)
    hash_results = hash_str + ' ' + base_filename
    debug('sidecar contents: ' + hash_results)
        with open(sidecar_path, 'wt') as f:
            f.write(hash_results)
    except OSError as e:
        critical(e, 'Problems creating sidecar hash file')
    debug('Finished creating sidecar file: ' + sidecar_path)
def create_sidecar_hash_files(path):
    '''For a given directory 'path', create a 'side-car' hash file for each file.
    Intended to be used in each Per-Tool-Directory (PTD), where tools
    are run, some and generate multiple files (eg, rom.bin, ACPI tables, ...)
    This code creates a 'side-car' hash file for each generated file
    (eg, rom.bin.sha256 for rom.bin, output.txt.sha256 for output.txt, ...).
    Run this before generating that directory's manifest.txt file.
    After running this, don't create any new files or modify any
    existing files in this directory. ...except for modifying file
    owner/group/attributes in the Unix sudo case.

    Returns True if successful, False if unsuccessful.'''
    # XXX Support (or fail with errors): dirs, files with links.
    # XXX can a hash have a space in it, which would require escaping?
    # XXX Support file with spaces or otherwise needing escaping
    # XXX How does sha256sum handle escaping files (eg, with spaces)?
    # XXX What other file formats are needed (eg, XML for one MSFT tool)?
    if is_none_or_null(path):
        error('Directory name to hash unspecified')
    if not dir_exists(path):
        error('Directory to hash does not exist: ' + path)
    debug('dir to hash: ' + path)
    hash_fn = None
        for root, dirs, files in os.walk(path):
            debug('root dir = ' + root)
            for fn in files:
                fqfn = path + os.sep + fn
                debug('file loop: filename = ' + fn)
                debug('file loop: fully-qualified filename = ' + fqfn)
                create_sidecar_hash_file(fqfn)
    except OSError as e:
        critical(e, 'Failed to create hash file')
    # XXX propogate status code upstream
    return True
        critical(e, 'Unexpected exception invoking process')
        critical(e, 'Unexpected exception occurred')
        critical(e, 'Unexpected exception occurred walking directory')

                if os_is_macos():
                    _dir = os.path.expanduser('~') + '/'
                else:
                    _dir = '/home/' + _sudo_user + '/'
                debug('Parent Dir (updated for SUDO usage) = ' + _dir)
def set_groups(path, new_uid, new_gid, verbose=True):
        # os.setgroups(new_gid_list)  # XXX macOS: ValueError: too many groups
        os.setgroups([new_gid_list[0]])  # XXX macOS: ValueError: too many groups
        critical(e, 'Unable to to update UID on file: ' + path)
        critical(e, 'Unable to update GID on file: ' + path)
        critical(e, 'Unable to modify mode on path: ' + path)
    debug('new file mode: ' + str(new_file_mode))
    debug('new dir mode: ' + str(new_dir_mode))
        debug('root dir = ' + root)
            debug('dir = ' + d)
            debug('joined dir = ' + joined)
            debug('file = ' + f)
            joined = os.path.join(root, f)
            debug('joined file = ' + joined)
        except OSError as e:
            critical(e, 'Problems creating per-tool-directory')
            error('Parent directory was not created')
        critical(e, 'Failed to create parent directory: ' + pd)

            critical(e, 'OSError trying to create tool directory')
        if app_state['hash_mode']:
            if not create_sidecar_hash_files(ptd):
                error('Unable to create side-car hash file(s) in PTD directory: ' + ptd)
                return False
        if app_state['manifest_mode']:
            debug('***** MANIFEST MODE:.....')
            if not create_manifest_file(ptd):
                error('Unable to create PTD manifest file in directory: ' + ptd)
                return False
    erc = rc  # XXX mock success, fix properly!
    # XXX Post 0.0.2, replace this ugly code with:
    elif tool == 'INTEL-SA-00075-Discovery-Tool':
        rc = intel_amt_discovery(toolns, tool, prd, ptd, erc)
    elif tool == 'intel_sa00086.py':
        rc = intel_me_detection(toolns, tool, prd, ptd, erc)
def diagnose_groups(uid_name_string, gid_name_string):
    '''TBW'''
    # XXX test when user and/or root is a member of multiple groups
    # test if macOS/FreeBSD behavior is the same as Linux. See the Python
    # documentation Note for os.getgroups() and os.setgrups().
    for (name, passwd, gid, members) in grp.getgrall():
        debug('name=' + name + ',  gid=' + str(gid) + ', members=' + str(members))
        # if username in members: gids.append(gid)
    all_groups = grp.getgrall()
    # output_wrapped(all_groups)
    # debug(str(all_groups))
    #for g in all_groups:
        #output_wrapped(str(g))
        # debug(str(g))
    groups = os.getgroups()
    #for g in groups:
        #output_wrapped(str(g))
        # debug(str(g))
    gname = gid_name_string
    uname = uid_name_string
    print('uname: ' + uname)
    print('gname: ' + gname)

    if not os_is_macos():
        gid = int(grp.getgrnam(gname)[2])
        uid = int(grp.getgrnam(gname)[2])
        print('grname uid: ' + str(uid))
        print('grname gid: ' + str(gid))

        uid = int(pwd.getpwnam(uname).pw_uid)
        gid = int(grp.getgrnam(gname).gr_gid)
        print('pwname uid: ' + str(uid))
        print('grname gid: ' + str(gid))

    cur_uid = os.getuid()
    cur_uid_name = pwd.getpwuid(os.getuid())[0]
    cur_gid = os.getgid()
    cur_group = grp.getgrgid(os.getgid())[0]
    print('uid: ' + str(cur_uid))
    print('uid name: ' + str(cur_uid_name))
    print('gid: ' + str(cur_gid))
    print('group: ' + str(cur_group))


        critical(e, 'showenv: OSError exception occurred')
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'memconfig']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'remap']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'smm_dma']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.secureboot.variables']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.uefi.access_uefispec']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.uefi.s3bootscript']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.bios_kbrd_buffer']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.bios_smi']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.bios_ts']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.bios_wp']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.ia32cfg']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.rtclock']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.smm']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.smrr']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.spi_desc']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.spi_fdopss']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-m', 'common.spi_lock']
    cmd = ['python', '-i', '-m', 'chipsec_main', '-i', '-n', '-m', 'tools.uefi.blacklist', '-a', ',' + blacklist_file]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'acpi', 'list']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'acpi', 'table', 'acpi_tables.bin']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'platform']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'cmos', 'dump']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'cpu', 'info']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'cpu', 'pt']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'decode', 'types']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'decode', spi_bin]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'ec', 'dump']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'io', 'list']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'iommu', 'list']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'iommu', 'status', iommu_engine]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'iommu', 'config', iommu_engine]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'iommu', 'pt']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'mmio', 'list']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'pci', 'enumerate']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'pci', 'dump']
    cmd = ['python', '-i', '-i', '-m', 'chipsec_util', 'pci', 'xrom']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'spd', 'detect']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'spd', 'dump']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'spi', 'dump', filename]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'spi', 'info']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'spidesc', filename]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'ucode', 'id']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'types']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'var-list']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'decode', filename]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'tables']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'keys', filename]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 's3bootscript']
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'nvram', filename]
    cmd = ['python', '-i', '-m', 'chipsec_util', 'uefi', 'nvram-auth', filename]
# intel_amt_discovery.py

# Detect Intel SA-00075 aka: CVE-2017-5689 AMT vulnerability


def intel_amt_discovery(toolns, tool, prd, ptd, erc):
    '''Run live command: 'INTEL-SA-00075-Discovery-Tool'.'''
    if not os_is_linux():
        error(tool + ' only works on Linux')
        return -1  # XXX generate exception
    info('Executing ' + toolns + ' variation of tool: ' + tool)
    cmd = [tool]
    return spawn_process(cmd, ptd, erc, toolns)

#####################################################################

# intel_me_detection.py

# Detect Intel SA-00086 aka: 
# CVE-2017-5705,CVE-2017-5708,CVE-2017-5711,CVE-2017-5712,CVE-2017-5706,CVE-2017-5707,CVE-2017-5709,CVE-2017-5710,CVE-2017-5706,CVE-2017-5709 
# Intel ME vulnerability

def intel_me_detection(toolns, tool, prd, ptd, erc):
    '''Run live command: ''intel_sa00086.py'.'''
    if not os_is_linux():
        error(tool + ' only works on Linux')
        return -1  # XXX generate exception
    info('Executing ' + toolns + ' variation of tool: ' + tool)
    cmd = [tool]
    return spawn_process(cmd, ptd, erc, toolns)

#####################################################################


#####################################################################
# manifest.py

#    buf = None
#    for fn in generated_files:
#        buf += hash_line
#        # calc hash
#        # with open('manifest.txt', 'wt', encodin='utf-8') as f:
#        f = open('manifest.txt', 'wt', encodin='utf-8')
#        f.write(buf)
#        f.close()

                hash_buf = return_hash_str_of_file(joined)
                if is_none_or_null(hash_buf):
                    error('Hash buffer is null')
                    m.close()
                    return False
                debug('make_manifest: hash string: ' + hash_buf)
        critical(e, 'IOError: Failed to create manifest file: ' + fn)
        critical(e, 'OSError: Failed to create manifest file: ' + fn)

#####################################################################