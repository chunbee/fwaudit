Firmware Audit, v0.0.2-PRE-ALPHA
Firmware Audit is a firmware analysis tool which calls multiple tools
(eg, CHIPSEC, FWTS, etc.) and gathers the results for forensic analysis.
WARNING: This is the 2 public release of this tool, aka Milestone2.
You should hold off until Milestone 3, when it should be more stable
# XXX new bugs/issues from 0.2:
# BUG: stdio file has "<toolname>." prefix, remove. Eg, lspci.stdout.txt should be stdout.txt.
# BUG: Python's os.getgroups() and os.setgroups() behave differently on Linux than on MacOSX. Need to ensure that the sudo code works on Mac.
# BUG: Syslog (and eventually EventLog) output is a mirror of stdout, too much spew for syslog.  Update syslog output to be: list of tools run with status, list of generated files with hashes, aka the index/report.
# BUG: everyplace a file is opened, should first check for a max size, in case file is huge. Unclear how big some rom.bins get. Need a user-specifed max, and understand the various system max values.
# BUG: After initial creation of dir, don't keep updating owner/group/file-mode each run, only do that once.
# BUG: global: standardize use of exceptions, int and bool return codes, some rcs overwritten raise LookupError("Invalid user: {!r}".format(foo))
# BUG: CHIPSEC blacklist args not working, get_tool_arg()/set_tool_arg() list/dict issue.
# TEST:  test sidecar hash file format against sha256sum tool.
# TEST: sudo use with a user account and/or a root account that has multiple group memberships.
# TEST: sidecar hash files against sha26sum
# TEST: manifest files against sha256sum (or ??)
# DOC: If SUDO used so that no SUDO_* environment variables are used, this code will not work.
# DOC: The --output_dir command currently only works for the root user, not the sudo case.


import stat
import pwd
import grp
import getpass

EVENTLOG_AVAILABLE = True
try:
    import windows_eventlog  # XXX proper module name
except ImportError:
    EVENTLOG_AVAILABLE = False
__version__ = '0.0.2'
    'home_page': '<https://preossec.com/>',  # XXX create/test
    'date': '2018-08-03 19:46',
    'output_dir_specified': False,  # user specifed explicit PD using --output_dir
    'hash_mode': False,  # --hash, --nohash
    'manifest_mode': False,  # --manifest, --nomanifest
    'max_buf': 50000,  # XXX add way to override? Proper value? subprocess
    'sudo_based_usage': False,
    'output_dir_specified': False,
# Need per-OS filenames, eg 'acpidump', 'acpidump.exe', 'acpidump.efi'.

    # Check if not a TTY?
        error('No tool(s) or profile selected, use --tool or --profile.')
    # XXX If only doing offline analysis, don't need to be root.
    # Defer root check until after determined what tools are selected,
    # if each can be run as non-root, then proceed, else this error path.
    # Will need a boolean in the TOOLS and/or PROFILE struct, or at least
    # the resulting generated tool list, showing if tool is Live or Offline,
    # and if tool requires Root or not. Most live tools require root, a few do not.
    if not is_user_root():
        return 1  # XXX generate exception

    if is_sudo_root():
        # debug('Configuring for SUDO usage')
        app_state['sudo_based_usage'] = True

        # start_results()  # XXX

        # Run the tools!
        # Post-processing, after running the tools
        # Create manifest of PD? No files, only dirs.
        # Create manifest of PRD? No files, only dirs.
        if is_sudo_root():
            # XXX need to fix PD dir perms, on first creation?
            debug('Changing SUDO root ownership/permissions to generated files..')
            if not change_generated_file_perms(prd):
                tool_status = 1
                error('Error occurred during chmod/chgrop post-processing')

        # create_shellscript()  # XXX
        # XXX create index file, with header, records, and footer of metadata.
        # enable zipped results, if user specified.
        # XXX Delete dir after creating zip.
        # if app_state['zip_results']:  # XXX
        #    debug('Creating ZIP file of results..')  # XXX
        #    zip_results()  # XXX
############################################################
    p.add_argument('--eventlog',
                   action='store_true', default=False,
                   help='Send hashes over Windows EventLog.')
                   help='Specify how to log tool output. IN 0.1 RELEASE USE FOR ROOT ONLY, DO NOT USE WITH SUDO USER.')
    p.add_argument('--manifest',
                   action='store_true', default=False,
                   help='Generate manifest file of hashes for generated files. DO NOT USE IN 0.1 RELEASE.')
    p.add_argument('--nomanifest',
                   action='store_true', default=False,
                   help='Do not generate manifest files.')
                   help='Generate SHA256 sidecar hash files for generated files. DO NOT USE IN 0.1 RELEASE.')
    p.add_argument('--nohash',
                   action='store_true', default=False,
                   help='Do not generate sidecar hash files.')
    if args.eventlog:
        app_state['eventlog_mode'] = True
    if args.syslog:
        app_state['syslog_mode'] = True
    if args.nohash:
        app_state['hash_mode'] = False
    if args.manifest:
        app_state['manifest_mode'] = True
    if args.nomanifest:
        app_state['manifest_mode'] = False
        app_state['output_dir'] = args.output_dir
        app_state['output_dir_specified'] = True
        info('User has specified explicit parent directory of: ' + app_state['output_dir'])
    if app_state['eventlog_mode']:
        eventlog_send(APP_METADATA['short_name'] + ': starting...')
    logmsg = None
        if app_state['verbose']:
            log('Program completed successfully')
        if app_state['verbose']:
            log('Program completed with error(s), status: ' + str(status))
    if app_state['eventlog_mode']:
        eventlog_send(logmsg)
        output('[ERROR] msg too long to log!, msg length=' + str(len(msg)) + ', max=' + str(max_buf) + '!')
        if (is_none_or_null(prefix_fg_color)) or ((is_none_or_null(prefix_bg_color))):
        if (is_none_or_null(msg_fg_color)) or ((is_none_or_null(msg_bg_color))):
    if app_state['eventlog_mode']:
        eventlog_send(prefix + msg + suffix)
def eventlog_send(msg):
    debug('FIXME: implement eventlog handler')
    '''Mirrors log message output to eventlog, on Windows systems.
    
    Returns True if it worked, False if fails.
    '''
    # XXX Test string buffer limits before sending to eventlog
    if not EVENTLOG_AVAILABLE:
        output('[ERROR] Windows eventlog Python module not available!')
        return False
    if not os_is_windows():
        output('[ERROR] eventlog only available for Windows systems!')
        return False
    if not app_state['eventlog_mode']:
        output('[ERROR] eventlog code called but eventlog_mode False!')
        return False
    if is_none_or_null(msg):
        output('[ERROR] Empty message, nothing to send to eventlog!')
        return False
    try:
        # XXX eventlog.eventlog(msg)
        return True
    except:
        output('[ERROR] Logger failed to send message to Windows EventLog!')
        sys.exc_info()
        output('[WARNING] Disabling Windows EventLog mode after first error.')
        app_state['eventlog_mode'] = False
        return False
    return True


        output('[ERROR] syslog only available for UNIX-based systems!')
        return False
    if not SYSLOG_AVAILABLE:
        output('[ERROR] syslog Python module not available!')
        output('[ERROR] Empty message, nothing to send to syslog!')
        final_msg = APP_METADATA['short_name'] + ': ' + msg
        # print('[DEBUG] syslog message: ' + final_msg)
        syslog.syslog(final_msg)
        return True
        error('Hash sidecar file already exists! Not overwriting')
        # _ign = warn_if_overwriting_file('create_sidecar_hash_file', hash_file_name)
        if is_none_or_null(hash_buf):
            error('create_sidecar_hash_file(): hash_buf is null or none')
            return False
        # sha256sum file format: <hash> + <space> + <filename>
        # XXX what about dirs? OS-specific path separators? escaping paths with spaces and other punct?
        # XXX what tools do Windows users use, certutil.exe, ...? what formats do they expect?
        # XXX Maybe add --hash_format=<toolname>, where <toolname> is sha256sum, certutil, ...
        hash_file.write(hash_buf + ' ' + filename_being_hashed)  # XXX newline?
    except OSError:
    input_ascii_file -- input filename
    ascii_file_hash_file -- output filename
    Returns True if file was written, False if failed.
        error('Unable to generate hash file, no input filename provided')
        return False
    if ascii_file_hash_file is None:
        error('Unable to generate hash file, no output filename provided')
        debug('create_hash_file: hash=' + digest_string + ', filename=' + ascii_file_hash_file)
        error('Unable to generate hash file, unexpected exception')
        debug('File name to be hashed: ' + filename)
        debug('File size (bytes) to be hashed: ' + str(file_size_bytes))
    '''TBW.'''
def list_profile_list(profiles, profile_name):
    if (new_profiles is not None) and (new_profiles is not ''):
def list_tools():
def get_tool_arg(toolns, key):
    '''Return argument of a tool, given a toolns.

    TOOLS['chipsec_iommu_engine']['args'] = args.chipsec_iommu_engine
    TOOLS['chipsec_util_spi_dump']['args'] = args.chipsec_rom_bin_file
    value = get_tool_arg(toolns, key)
    Remove this once I can figure out how to use Python dictionaries properly.
    '''
    # arg_value = TOOLS[tool_ns]['args'][arg_key]
    # debug('toolns=' + tool_ns + ', arg_key=' + arg_key + 'arg_value=' + arg_value)
    # XXX need to add key after args!!
    if is_none_or_null(toolns):
        error('Tool namespace not specified')
        return None
    if not is_valid_tool(toolns):
        error('Invalid tool namespace: ' + toolns)
        return None
#    for t in TOOLS:
#        tool_name = t['tool']
#        ns = t['name']
#        tool_args = t['args']
#        if not isinstance(expected_rc, int):
#            error('Expected RC is not an Integer')
#            return (None, None)
#        if toolns == ns:
#            debug('SUCCESS, valid tool ' + tool_name + ', args= ' + str(tool_args))
#            return tool_args
#    error('Invalid toolns: ' + toolns)
    # Traverse TOOLS list, finding toolns entry.
    for i, t in enumerate(TOOLS):
        #tool_name = t['tool']
        tool_ns = t['name']
        tool_args = t['args']
        #tool_expected_rc = t['exrc']
        if tool_ns == toolns:
            # debug('Valid tool ' + tool_ns)
            try:
                value = tool_args[key]
                debug('Toolns=' + toolns + ', key=' + key + ', value=' + value)
                return value
            except KeyError:
                debug('KeyError exception, key not valid: ' + key)
                return None
            debug('Tool not found!')
    return None


        tool_ns = t['name']
        tool_args = t['args']
        if tool_ns != toolns:
            debug('Valid tool ' + tool_ns)
                value = tool_args[key]
    error('Invalid tool ' + toolns)
def is_valid_tool(lookup_name):
        tool_ns = t['name']
        # debug('is_valid_tool(): tool_name = ' + tool_ns)
        if tool_ns == lookup_name:
            # debug('Valid tool ' + lookup_name)
    error('Invalid tool ' + lookup_name)

    debug('pre-exec: tool="' + args[0] + '", ns="' + toolns + '", cwd="' + start_dir + '"')
            debug(status_string + ': ' +
    if app_state['syslog_mode']:
            # debug('Logging stdout to syslog..')
    if app_state['eventlog_mode']:
        debug('Logging exec results to Windows EventLog..')
        eventlog_send(log_msg)
def get_parent_directory_name():
    '''Get the name of the Parent Directory (PD).

    Sets app_state['output_dir'], if user has not already specified an directory
    via --output_dir. On Unix, when sudo used, dir is changed from root-based to
    pre-sudo user-based.

    Return True if successful, False if there was a problem.'''
    # XXX Does upstream code test if dir does not exist, and create or fail?
    if app_state['output_dir_specified']:
        debug('User specified output dir')
        _dir = app_state['output_dir']
        if is_none_or_null(_dir):
            error('User-specified parent directory is empty')
            return False
    else:
        _dir = get_default_directory_name()
        if is_none_or_null(_dir):
            error('Directory is null')
            return False
        # Note: returned path has trailing path separator (/, \)!
        app_state['output_dir'] = _dir + 'fwaudit.results'
    debug('Output parent directory: ' + app_state['output_dir'])
    return True

def get_default_directory_name():
    '''Get the name of the directory where the Parent Directory is.

    Get the OS-centric directory name where the 'Parent Directory' (PD) is located.
    Note: Downstream code presumes trailing path separator.

    Return string of dir, or None if failure.'''
    _dir = None
    if os_is_unix():
        if app_state['sudo_based_usage']:
            try:
                _sudo_user = os.getenv('SUDO_USER')
                if is_none_or_null(_sudo_user):
                    error('SUDO_USER environment variable is null')
                    return None
                _dir = '/home/' + _sudo_user + '/'
                #debug('Parent Dir (updated for SUDO usage) = ' + _dir)
            except:
                error('Unable to get SUDO user home directory')
                sys.exc_info()
                return None
        else:
            try:
                _dir = os.environ['HOME']
                _dir = _dir + '/'
                #debug('Parent Dir (NOT updated for SUDO usage) = ' + _dir)
            except:
                error('Unable to get HOME environment variable')
                sys.exc_info()
                _dir = None
            if is_none_or_null(_dir):
                error('HOME environment variable is empty')
                _dir = None
    elif os_is_windows():
        debug('Getting dir of Windows system')
        _dir = '%APPDATA%\\Roaming\\'  # XXX untested codepath!
    elif os_is_uefi():
        debug('Getting dir of UEFI Shell system')
        _dir = 'fs0:\\'  # XXX untested codepath!
    else:
        error('Unsupported target OS')
        _dir = None
    if is_none_or_null(_dir):
        error('Generated home directory is null')
    return _dir


def sudo_user_diags():
    '''For Unix SUDO use case, get pre-SUDO username.'''
    # What is FSB/POSIX standard for '/home/' + username?
    # win32api: GetUserName() and GetUserNameEx()
    # Is root always 0 (EUID==0?) on all modern *nix systems?
    # How to deal with Linux Capabilities?
    # How to deal with SELinux?
    # How to deal with Linux ACLs?
    # How to deal with BSD...?
    try:
        sudo_user = os.getenv('SUDO_USER')
        debug('getenv(SUDO_USER) username: ' + sudo_user)
        sudouser_home_dir = '/home/' + sudo_user
        debug('Homedir = ' + sudouser_home_dir)
    except:
        debug('Unable to view SUDO_USER')
    user = os.getenv('USER')
    logname_username = os.getenv('LOGNAME')
    # username = pwd.getpwuid(os.geteuid()).pw_name
    pwname_username = pwd.getpwuid(os.getuid()).pw_name
    username = getpass.getuser()
    userhome = os.path.expanduser('~')
    debug('getenv(LOGNAME) username: ' + logname_username)
    debug('pwd.getpwuid.pw_name: ' + pwname_username)
    debug('getpass.getuser() username: ' + username)
    debug('expanduser(~) home dir: ' + userhome)
    debug('getenv(USER) username: ' + user)
    logname_home_dir = os.path.expanduser('~' + logname_username + '/')
    debug('Homedir = ' + logname_home_dir)
    pwname_home_dir = os.path.expanduser('~' + pwname_username + '/')
    debug('Homedir = ' + pwname_home_dir)


def set_groups(path, new_uid, new_gid, verbose=False):
    '''For sudo case, set GID to non-SuperUser value.'''
    if not app_state['sudo_based_usage']:
        debug('set_groups: called for non-sudo use')
        return False
    try:
        debug('Changing file owner: file=' + path + ', uid=' + str(new_uid))
        new_gid_list = []
        new_gid_list = os.getgroups()
        if verbose:
            debug('os.getgroups: new_gid_list: ' + str(new_gid_list))
        os.setgroups([])
        if verbose:
            debug('calling os.setgroups(' + str(new_gid_list) + ')..')
        os.setgroups(new_gid_list)
        if verbose:
            debug('calling os.setgid(' + str(new_gid) + ')..')
        os.setgid(new_gid)
    except OSError as e:
        sys.exc_info()
        error('Unable to to update UID on file: ' + path)
        log('Exception ' + str(e.errno) + ': ' + str(e))
        return False
    return True


def set_owner(path, new_uid, new_gid):
    '''For sudo case, set UID to non-SuperUser value.'''
    if not app_state['sudo_based_usage']:
        debug('set_owner: called for non-sudo use')
        return False
    try:
        debug('Changing file owner: file=' + path + ', uid=' + str(new_uid))
        os.chown(path, new_uid, new_gid)
    except OSError as e:
        sys.exc_info()
        debug('Unable to update GID on file: ' + path)  # XXX error()
        debug('Exception ' + str(e.errno) + ': ' + str(e))  # XXX log()
        return False
    return True


def change_file_owner_group(path, new_uid, new_gid):
    '''For Unix SUDO use case, modify existing root-owned file to pre-SUDO user.'''
    if not app_state['sudo_based_usage']:
        debug('set_owner: called for non-sudo use')
        return True
    if path is None:
        error('No path specified')
        return False
    if new_uid is None:
        error('No UID specified')
        return False
    if new_gid is None:
        error('No GID specified')
        return False
    debug('Changing file owner/group/mode: ' + path + ',' + str(new_uid) + ', ' + str(new_gid))
    owner_status = set_owner(path, new_uid, new_gid)
    group_status = set_groups(path, new_uid, new_gid)
    if (not owner_status) or (not group_status):
        debug('Unable to set file ownership/group')  # XXX error()
        return False
    return True


def change_file_mode(path, new_mode):
    '''For Unix SUDO use case, modify existing file attributes.'''
    # XXX how to determine which to set, user or sudo?
    if not app_state['sudo_based_usage']:
        debug('Not updating file mode, not using sudo')
        return True
    if path is None:
        error('No path specified')
        return False
    if new_mode is None:
        error('No file mode specified')
        return False
    try:
        os.chmod(path, new_mode)
    except OSError as e:
        sys.exc_info()
        debug('Unable to modify mode on path: ' + path)  # XXX error()
        debug('ERROR: Exception ' + str(e.errno) + ': ' + str(e))  # XXX log()
        return False
    return True


def change_generated_file_perms(path, verbose=False):
    '''Change file ownership of a sudo-created file to it's non-root user.

    After the tools have been run, traverse the per-run-directory (PRD)
    and update all the files that the tools have generated, fixing the
    file ownerships from sudo'ed 'root' to the actual user, so the user
    can view the resulting files w/o having to become superuser.
    Eg: change_owner_and_attributes("rom.bin", "nobody", "nogroup", 436)

    Returns 0 if successful, 1 if an error occurred.'''
    if not app_state['sudo_based_usage']:
        debug('Not updating file owner/group/mode, not using sudo')
        return True
    if not os_is_unix():
        error('Only for UNIX-style OSes')
        return False
    cur_uid = os.getuid()
    if cur_uid != 0:
        error('UID nonzero: User is not SuperUser')
        return False
    debug('current UID: ' + str(cur_uid))
    cur_euid = os.geteuid()
    if cur_euid != 0:
        error('EUID nonzero: User is not SuperUser')
        return False
    debug('current EUID: ' + str(cur_euid))
    if path is None:
        error('Must specify path to set')
        return False

    # XXX This whole section: duplicate code, use existing function
    new_uid = int(os.environ.get('SUDO_UID'))
    if new_uid is None:
        error('Unable to obtain SUDO_UID')
        return False
    new_gid = int(os.environ.get('SUDO_GID'))
    if new_gid is None:
        error('Unable to obtain SUDO_GID')
        return False
    # XXX Read-only works for FILE, but need Write support for DIRs.
    # new_mode = ( stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH )
    # new_mode = stat.S_IREAD | stat.S_IRUSR | stat.S_IRGRP
    r_mode = (stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
    rw_mode = (stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH)
    rwx_mode = (stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO) 
    new_dir_mode = rwx_mode
    new_file_mode = rwx_mode
    if verbose:
        debug('new file mode: ' + str(new_file_mode))
    if verbose:
        debug('new dir mode: ' + str(new_dir_mode))

    for root, dirs, files in os.walk(path):  
        if verbose:
            debug('root dir = ' + root)
        for d in dirs:  
            if verbose:
                debug('dir = ' + d)
            joined = os.path.join(path, d)
            if verbose:
                debug('joined dir = ' + joined)
            change_file_owner_group(joined, int(new_uid), int(new_gid))
            change_file_mode(joined, int(new_dir_mode))

        for f in files:
            if verbose:
                debug('file = ' + f)
            joined = os.path.join(path, f)
            if verbose:
                debug('joined file = ' + joined)
            change_file_owner_group(joined, int(new_uid), int(new_gid))
            change_file_mode(joined, int(new_dir_mode))
    # XXX propogate status code upstream
    return True


def build_meta_profile(verbose=True):
    # XXX can also check for dup tools when creating ptd, check if already exists.
    # XXX Remove verbose arg, or at least sync with global.
    if (app_state['user_profiles'] is None) and (app_state['user_tools'] is None):
        error('No profile(s) or tool(s) selected, nothing to do')
    if (app_state['no_profile']) and (app_state['new_profiles'] is None):
        warning('Profiles are disabled')
        # XXX this codepath previously returned False. Does any below code presume the previous return?
    # Enumerate user selected tool(s) list.
        if verbose:
            output_wrapped(app_state['user_tools'])
                debug('Adding tool to meta_profile: ' + t)
    # Enumerate user-selected profile(s) list.
            debug('Examining user-defined profiles')
            info('Examining built-in profiles')
                if verbose:
                    info('Profile: ' + str(type(p['name'])))
                info('Profile: ' + p['name'])
                    if verbose:
                        info('Matches profile: ' + p['name'])
                            if verbose:
                                info('Adding tool to meta_profile: ' + t)
                            skipped += 1
    debug('Tool count: ' + str(tools))
    debug('Skipped count: ' + str(skipped))
    '''Setup PD and PTD, including dealing with SUDO root -vs- user dir.

    Return True if successful, False if not.'''

    (new_dir_mode, new_uid, new_gid) = get_sudo_user_group_mode()

    # Part 1 of 3:
    # Get the name of PD
    _dir = get_parent_directory_name()
    if is_none_or_null(_dir):
        error('Parent directory name unspecified')
        return False, None, None
    # Create PD
    if setup_parent_directory(new_dir_mode, new_uid, new_gid) is False:

    # Part 2 of 3:
    if not setup_per_run_directory(pd, new_dir_mode, new_uid, new_gid):

    # Part 3 of 3: the Per-Tool-Directories (PTDs), happens elsewhere.

def setup_per_run_directory(pd, new_dir_mode, new_uid, new_gid):
    # XXX UCT timezone usage
    stamp_format = '%Y%m%d%H%M%S' # '%Y%m%d_%H%M%S_%f'
    timestamp = time.strftime(stamp_format, ts)
    debug('Per-run-directory: ' + prd)
    if app_state['sudo_based_usage']:
        debug('Changing owner/group of PRD...')
        change_file_owner_group(prd, new_uid, new_gid)
        debug('Changing attribs of PRD...')
        change_file_mode(prd, new_dir_mode)
    return True


def get_sudo_user_group_mode():
    '''TBW'''
    # XXX only need uid, gid, and file mode for sudo case...
    new_uid = int(os.environ.get('SUDO_UID'))
    if new_uid is None:
        error('Unable to obtain SUDO_UID')
        return False
    #debug('new UID via SUDO_UID: ' + str(new_uid))
    new_gid = int(os.environ.get('SUDO_GID'))
    if new_gid is None:
        error('Unable to obtain SUDO_GID')
        return False
    #debug('new GID via SUDO_GID: ' + str(new_gid))
    # new_dir_mode = (stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH)
    rwx_mode = (stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    new_dir_mode = rwx_mode
    #debug('new dir mode: ' + str(new_dir_mode))
    return (new_dir_mode, new_uid, new_gid)


def setup_per_tool_directory(pd, prd, ptd, toolns):
    '''Create the per-tool directory.'''
    if is_none_or_null(ptd):
        error('Per-tool-directory name unspecified')
        return False
    if dir_exists(ptd):
        if not is_dir_empty(ptd):
            error('Skipping non-empty per-tool-directory: ' + ptd)
            return False
        warning('Using existing empty per-tool directory: ' + ptd)
    else:
        try:
            os.mkdir(ptd)
            if not dir_exists(ptd):
                error('Problems creating per-tool-directory')
                return False
        except OSError:
            sys.exc_info()
            error('Problems creating per-tool-directory')
            return False

    (new_dir_mode, new_uid, new_gid) = get_sudo_user_group_mode()
    change_file_owner_group(ptd, new_uid, new_gid)
    change_file_mode(ptd, new_dir_mode)
    if not dir_exists(ptd):
        error('Target per-tool directory was not created: ' + ptd)
        return False
def setup_parent_directory(new_dir_mode, new_uid, new_gid):
    If Unix user has used SUDO to become SuperUser, then the 
    PD must be changed from default root-based to original user-based,
    so after SUDO command, the resulting files are in the user's 
    subdir, not in the root dir.

    If user specifies their own PD, then should not modify location.

    What to do if user foo has an existing PD, and ALSO the root
    has an existing PD? Two users separately using fwaudit, two
    separate datasets. Warn? Merge? How to fail properly?
    # By now, PD string should exist. Create dir, if it doesn't already exist.
    if dir_exists(pd):
        debug('Parent directory already exists: ' + pd)
        return True
    debug('Parent directory does not exist, creating: ' + pd)
    try:
        os.mkdir(pd)
        if not dir_exists(pd):
    except OSError as e:
        sys.exc_info()
        error('Problems creating parent directory')
        return False
    # XXX only do this if using sudo codepath
    debug('Updating owner/attribs of Parent Directory')
    change_file_owner_group(pd, new_uid, new_gid)
    change_file_mode(pd, new_dir_mode)

    return True
    # For each tool to run, create it's target per-tool-directory.
            if not setup_per_tool_directory(pd, prd, ptd, toolns):
                error('Unable to create per-tool-directory')
                debug('Created per-tool directory: ' + ptd)
            sys.exc_info()
            # XXX: check if OSError is File Not Found
        # Call tool resolver, to determine which variation (namespace) of a tool to run
        rc = tool_resolver(toolns, pd, prd, ptd)
        # XXX Confirm failure rc is logged in tool_resolver() or finish_results()
        debug('Post-tool-resolution, rc = ' + str(rc))

    if app_state['hash_mode']:
        if not create_sidecar_hash_files(ptd):
            error('Unable to create side-car hash file(s) in PTD directory: ' + ptd)
            return False
    if app_state['manifest_mode']:
        if not create_manifest_file(ptd):
            error('Unable to create PTD manifest file in directory: ' + ptd)
            return False
    # XXX propogate error upstream
    debug('Expected_rc=' + str(erc) + ', rc=' + str(rc))


    return rc
            # debug('SUCCESS, valid tool ' + tool_name)
    error('Unrecognized tool namespace: ' + toolns)
        error('Cannot check if path exists if the input is null')
            # info('File exists and is readable: ' + path)
        error('Unexpected exception verifying path: ' + path)
        debug('User is ROOT, UID: ' + str(uid))
        debug('User is NOT root, UID: ' + str(uid))
    if 'Darwin' in platform.system():
def is_sudo_root():
    '''Returns True if user is root via sudo, False if not.'''
    if not is_unix_user_root():
        error('User is not SuperUser')
        return False
    uid = os.getenv('SUDO_UID')
    if uid == None:
        error('No SUDO_UID set')
        return False
    # info('User is SUDO root')
    return True


        # show_sudo_vars()

        debug('SUDO_COMMAND = ' + command)
        debug('SUDO_USER = ' + user)
        debug('SUDO_UID = ' + uid)
        log('USER     = ' + user)
    debug('diagnosing root groups..')
    diagnose_groups("root", "root")
    #debug('diagnosing user groups..')
    #diagnose_groups("user", "user")
    print()
    sudo_user_diags()
    Check if OS is supported. adjust OS logging if not available.
    elif os_is_windows():
        debug('Windows codepath is untested..')
        if app_state['eventlog_mode'] and not EVENTLOG_AVAILABLE:
            warning('Windows EventLog module not available')
            info('Continuing with EventLog support disabled')
            app_state['eventlog_mode'] = False
        if app_state['syslog_mode']:
            warning('Windows does not support UNIX SysLog logging')
            info('Continuing with SysLog support disabled')
            app_state['syslog_mode'] = False
    XXX: Test if CHIPSEC will work uner PyPy.
             str(required_major) + '.' +
             str(required_minor) + ' is required')
    if (major != required_major) and (minor != required_minor):
    cmd = ['python', '-m', 'chipsec_main', '-m', 'memconfig']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'remap']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'smm_dma']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.secureboot.variables']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.uefi.access_uefispec']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.uefi.s3bootscript']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.bios_kbrd_buffer']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.bios_smi']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.bios_ts']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.bios_wp']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.ia32cfg']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.rtclock']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.smm']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.smrr']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.spi_desc']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.spi_fdopss']
    cmd = ['python', '-m', 'chipsec_main', '-m', 'common.spi_lock']
    cmd = ['python', '-m', 'chipsec_main', '-i', '-n', '-m', 'tools.uefi.blacklist', '-a', ',' + blacklist_file]
    cmd = ['python', '-m', 'chipsec_util', 'acpi', 'table', 'acpi_tables.bin']
    cmd = ['python', '-m', 'chipsec_util', 'cmos', 'dump']
    cmd = ['python', '-m', 'chipsec_util', 'cpu', 'info']
    cmd = ['python', '-m', 'chipsec_util', 'cpu', 'pt']
    cmd = ['python', '-m', 'chipsec_util', 'decode', 'types']
    cmd = ['python', '-m', 'chipsec_util', 'decode', spi_bin]
    cmd = ['python', '-m', 'chipsec_util', 'ec', 'dump']
    cmd = ['python', '-m', 'chipsec_util', 'io', 'list']
    cmd = ['python', '-m', 'chipsec_util', 'iommu', 'list']
    cmd = ['python', '-m', 'chipsec_util', 'iommu', 'status', iommu_engine]
    cmd = ['python', '-m', 'chipsec_util', 'iommu', 'config', iommu_engine]
    cmd = ['python', '-m', 'chipsec_util', 'iommu', 'pt']
    cmd = ['python', '-m', 'chipsec_util', 'mmio', 'list']
    cmd = ['python', '-m', 'chipsec_util', 'pci', 'enumerate']
    cmd = ['python', '-m', 'chipsec_util', 'pci', 'dump']
    cmd = ['python', '-m', 'chipsec_util', 'pci', 'xrom']
    cmd = ['python', '-m', 'chipsec_util', 'spd', 'detect']
    cmd = ['python', '-m', 'chipsec_util', 'spd', 'dump']
    cmd = ['python', '-m', 'chipsec_util', 'spi', 'dump', filename]
    cmd = ['python', '-m', 'chipsec_util', 'spi', 'info']
    cmd = ['python', '-m', 'chipsec_util', 'spidesc', filename]
    cmd = ['python', '-m', 'chipsec_util', 'ucode', 'id']
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'types']
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'var-list']
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'decode', filename]
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'tables']
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'keys', filename]
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 's3bootscript']
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'nvram', filename]
    cmd = ['python', '-m', 'chipsec_util', 'uefi', 'nvram-auth', filename]
# XXX acpixtract()


    rc = -1
        return rc
#####################################################################

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
    gid = int(grp.getgrnam(gname)[2])
    uid = int(grp.getgrnam(gname)[2])
    print('uid: ' + str(uid))
    print('gid: ' + str(gid))
    uid = int(pwd.getpwnam(uname).pw_uid)
    gid = int(grp.getgrnam(gname).gr_gid)
    print('uid: ' + str(uid))
    print('gid: ' + str(gid))
    cur_uid = os.getuid()
    cur_uid_name = pwd.getpwuid(os.getuid())[0]
    cur_gid = os.getgid()
    cur_group = grp.getgrgid(os.getgid())[0]
    print('uid: ' + str(cur_uid))
    print('uid name: ' + str(cur_uid_name))
    print('gid: ' + str(cur_gid))
    print('group: ' + str(cur_group))

#######################################

def do_hash(fn, hash_fn):
    '''TBW'''
    if is_none_or_null(fn):
        error('Cannot create hash file, filename to hash is null')
        return False
    if is_none_or_null(hash_fn):
        error('Cannot create hash file, hash filename is null')
        return False
    debug('do_hash_file: fn = ' + fn)
    debug('do_hash_file: hash_fn = ' + hash_fn)
    try:
        f = open(hash_fn, 'rb')  # encoding='utf-8' , errors='strict')
        # XXX test size before reading into memory
        file_buf = f.read()  # .decode('utf-8')
        f.close()
        if not is_none_or_null(file_buf):
            # hash_fn = fn + '.sha256'
            info('Creating side-car hash file: ' + hash_fn)
            create_sidecar_hash_file(fn, file_buf, hash_fn)
        file_buf = None
    except IOError as e:
        log('Exception ' + str(e.errno) + ': ' + str(e))
        error('Error while creating hash file')
        sys.exc_info()
        return False
    return True


def create_sidecar_hash_files(path):
    '''For each file in a directory, create a new side-car hash file.

    Intended to be used in each Per-Tool-Directory (PTD), where tools
    are run, some and generate multiple files (eg, rom.bin, ACPI tables, ...)
    This code creates a 'side-car' hash file for each generated file
    (eg, rom.bin.sha256 for rom.bin, output.txt.sha256 for output.txt, ...).

    Run this before generating that directory's manifest.txt file.
    After running this, don't create any new files or modify any
    existing files in this directory. ...except for modifying file
    owner/group/attributes in the Unix sudo case.
    Returns True if successful, False if an error occurred.'''
    # XXX Support (or fail with errors): dirs, files with links.
    # XXX can a hash have a space in it, which would require escaping?
    # XXX Support file with spaces or otherwise needing escaping
    # XXX How does sha256sum handle escaping files (eg, with spaces)?
    # XXX What other file formats are needed (eg, XML for one MSFT tool)?
    HASH_FILENAME_EXTENSION = '.sha256'
    if is_none_or_null(path):
        error('Cannot create hash files, directory is null')
        return False
    if not dir_exists(path):
        error('Cannot create hash files, directory does not exist: ' + path)
        return False
    hash_fn = None
    try:
        for root, dirs, files in os.walk(path):
            debug('create_hash_file: root dir = ' + root)
            for fn in files:
                joined = os.path.join(path, fn)
                hash_fn = joined + HASH_FILENAME_EXTENSION
                debug('create_hash_file: fn = ' + fn)
                debug('create_hash_file: joined = ' + joined)
                debug('create_hash_file: hash_fn = ' + hash_fn) 
                status = do_hash(joined, hash_fn)  # use joined for fn!
    except OSError as e:
        error('Failed to create hash file')
        log('Exception ' + str(e.errno) + ': ' + str(e))
        sys.exc_info()
        return False
    # XXX propogate status code upstream
    return True


def create_manifest_file(path):
    '''Create a manifest.txt for all files in a directory.

    Create a manifest.txt file, in the specified directory, and
    for each file in that directory, add one line to the manifest,
    with a line format of: "<hash> + <space> + <filename> + <newline>".

    Returns True if successful, False if an error occurred.'''
    # XXX MULTIPLE ISSUES in create_sidecar_hash_files() are identical to here!
    MANIFEST_FILENAME = 'manifest.txt'
    if path is None:
        error('Directory to create manifest for is null')
        return False
    if not dir_exists(path):
        error('Directory to create manifest for does not exist: ' + path)
        return False
    debug('make_manifest: path = ' + path)
    fn = path + os.sep + MANIFEST_FILENAME  # os.path.join()
    debug('Creating manifest file: ' + fn)
    if path_exists(fn):
        error('Not overwriting existing manifest file: ' + fn)
        return False
    try:
        # Open the manifest file
        debug('Opening manifest file: ' + fn)
        m = open(fn, 'wt')  # , encoding='utf-8')  # , errors='strict')
        for root, dirs, files in os.walk(path):
            debug('make_manifest: root dir = ' + root)
            # For each file, write one line to manifest file
            for f in files:
                debug('make_manifest: current file = ' + f)
                joined = os.path.join(path, f)
                debug('make_manifest: current joined file = ' + joined)
                # The next few lines can probably be replaced with a hash function
                f_fn = open(f, 'rb')  # , encoding='utf-8', errors='strict')
                file_buf = f_fn.read()
                f_fn.close()
                debug('make_manifest: x')
                hash_buf = hash_sha256_buffer(file_buf)
                # Check if hash_buf is null.

                manifest_line = hash_buf + ' ' + f + os.linesep
                if is_none_or_null(manifest_line):
                    error('Manifest record line is null!')
                debug('make_manifest: manifest line: ' + manifest_line)
                m.write(manifest_line)
                m.flush()
        debug('Closing manifest file')
        m.close()
    except IOError as e:
        error('IOError: Failed to create manifest file: ' + fn)
        log('Exception ' + str(e.errno) + ': ' + str(e))
        sys.exc_info()
        return False
    except OSError as e:
        error('OSError: Failed to create manifest file: ' + fn)
        log('Exception ' + str(e.errno) + ': ' + str(e))
        sys.exc_info()
        return False
    # XXX propogate status code upstream
    return True

#######################################