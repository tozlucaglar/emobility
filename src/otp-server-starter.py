import os, sys
import subprocess


def get_repo_root():
    """Get the root directory of the repo."""
    dir_in_repo = os.path.dirname(os.path.abspath('__file__'))  # os.getcwd()
    return subprocess.check_output('git rev-parse --show-toplevel'.split(),
                                   cwd=dir_in_repo,
                                   universal_newlines=True).rstrip()


ROOT_dir = get_repo_root()
sys.path.append(ROOT_dir)
sys.path.insert(0, ROOT_dir + '/lib')
import lib.routing as routing


if __name__ == "__main__":
    country = 'sweden'
    region = 'vg'
    # Start the server
    print('Start the OTP server...')
    otp_file = ROOT_dir + '/dbs/otp-2.2.0-shaded.jar'
    otp_folder = ROOT_dir + f'/dbs/{region}'
    memory_gb = 50  # assigned memory for java in GB
    routing.otp_server_starter(otp_file=otp_file, otp_folder=otp_folder, memory_gb=memory_gb)