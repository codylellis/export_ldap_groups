import subprocess

def info():

    global mdsip
    mdsip = input("Enter Management Server IP: \n")

def runcmd(cmd):

    script= f"""
#!/bin/bash

#Generic Check Point profile (Needed for most Check Point commands)
source /etc/profile.d/CP.sh

#VSX Profile (Needed for vsenv)
source /etc/profile.d/vsenv.sh

#MDS Profiles (Needed for mdsenv - dependent on /etc/profile.d/CP.sh)
source $MDSDIR/scripts/MDSprofile.sh
source $MDS_SYSTEM/shared/mds_environment_utils.sh

#Misc Profile
source $MDS_SYSTEM/shared/sh_utilities.sh

# Change to CMA context
mdsenv {mdsip}

# run command
{cmd}
"""

    exportscript=f'./{mdsip}_cpmiquery_ldap_groups.sh'

    with open(exportscript, 'w') as f:
        f.writelines(script)

    cmd=f'chmod +x {exportscript}; {exportscript}'
    stdout = subprocess.check_output(cmd, shell=True).decode('ascii').strip().splitlines()

    return stdout



# create dbedit file
def dbedit():

    dbfile=f"{mdsip}_ldapgroups_dbedit.txt"

    with open(dbfile, 'w+') as f:
        for n1,n2,n3,n4,n5 in zip(lname, lau, lldap, lbranch, lcolor):
            dbconfig=f"""create external_group {n1.strip()}
modify users {n1.strip()} Group_Scope Ldap_Group
modify users {n1.strip()} au servers:{n2.strip()}
modify users {n1.strip()} branch "{n4.strip()}"
modify users {n1.strip()} ldap_groupname "{n3.strip()}"
modify users {n1.strip()} color {n5.strip()}
update users {n1.strip()}
"""
            # print(f'dbconfig : {dbconfig}\n')
            f.write(dbconfig)

    with open(dbfile, 'a') as f:
        f.write("update_all\nquit")


if __name__ == "__main__":

    # ask for ip address for export
    info()

    # create lists for dbedit file
    lname = runcmd("""cpmiquerybin attr "" users "(class='external_group')" -a __name__""")
    lcolor = runcmd("""cpmiquerybin attr "" users "(class='external_group')" -a color""")
    lau = runcmd("""cpmiquerybin attr "" users "(class='external_group')" -a au | sed 's/(Table: servers)//g' | sed 's/Name://g' """)
    lldap = runcmd("""cpmiquerybin attr "" users "(class='external_group')" -a ldap_groupname""")
    lbranch = runcmd("""cpmiquerybin attr "" users "(class='external_group')" -a branch""")

    with open('lldap.txt', 'w') as a:
        a.writelines(lldap)

    print(f"LEN name : {len(lname)}\n")
    print(f"LEN au : {len(lau)}\n")
    print(f"LEN ldap : {len(lldap)}\n")
    print(f"LEN branch : {len(lbranch)}\n")
    print(f"LEN color : {len(lcolor)}\n")

    # create dbedit file
    dbedit()

