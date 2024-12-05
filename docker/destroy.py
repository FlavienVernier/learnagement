import os
import shutil
import subprocess

def main():
    
    if os.name == 'nt':
        prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose', 'down'],stdin=sp.PIPE)
        prog.stdin.write('password')
        prog.communicate()
    else:    
        subprocess.run(["sudo", "docker-compose", "down"], check=True)



    if os.name == 'nt':
        prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker', 'volume', 'rm', 'docker_learnagement_persistent_db'],stdin=sp.PIPE)
        prog.stdin.write('password')
        prog.communicate()
    else:            
        subprocess.run(["sudo", "docker", "volume", "rm", "docker_learnagement_persistent_db"], check=True)
        
    

if __name__ == "__main__":
    main()
