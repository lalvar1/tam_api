import os
import queue as queue
import pymssql


### Runs a SQL query and returns all results
def runQueryGetRows(queryString,server, resultsAsDict):
    with pymssql.connect(server) as conn:
        with conn.cursor(as_dict=resultsAsDict) as cursor:
            cursor.execute(queryString)
            return cursor.fetchall()

### Runs a SQL query and returns a single value
def runQueryGetValue(queryString, username, server, database, password):
    with pymssql.connect(server, username, password, database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(queryString)
            try:
                return cursor.fetchone()[0]
            except:
                return False

def getDevicesSQL(queue, server, resultsAsDict):
    queryStr = '''  SELECT DISTINCT CI_Name FROM [ITDW].[shared].[vw_NS_GRDB_CMDB_Network]
                    WHERE [ClassId] like 'BMC_ComputerSystem' 
                    AND [Category] like 'Network' 
                    AND ([Support Group] like '%Infrastructure-Foundation-Network/Voice%' or [Support Group] like  '%XTO-Network Operations%') 
                    '''
    #(CI_Name LIKE 'USEMC%' OR CI_Name LIKE 'USHHL%' OR CI_Name LIKE 'USBTN%')
    rows = runQueryGetRows(queryStr, server, True)
    nonDuplicatedHostnames = []
    for row in rows:
        if 'wlnwlc' in row['CI_Name'].lower():
            item = getFQDNAndIPAddress(row['CI_Name'].upper().split('.')[0])['fqdn']
        elif '-sec' in row['CI_Name'].lower() and not 'secsec' in row['CI_Name'].lower() and not 'secsic' in row['CI_Name'].lower() and not 'secsio' in row['CI_Name'].lower():
            item = getFQDNAndIPAddress(row['CI_Name'].upper().split('.')[0])['fqdn']
        else:
            item = getFQDNAndIPAddress(row['CI_Name'].upper().split('.')[0])['ip']
        if not item in nonDuplicatedHostnames:
            nonDuplicatedHostnames.append(item)
    for row in nonDuplicatedHostnames:
        queue.put(row)
    return

def getFQDNAndIPAddress(hostname, domainsList=None):
    if not domainsList:
        domainsList = ['.na.xom.com.', '.af.xom.com.', '.ea.xom.com.', '.sa.xom.com.', '.ap.xom.com.', '.ups.xom.com.', '.xtonet.com.']
    hostname = hostname.split('.')[0]
    region = domainsList.pop(0)
    fqdn = hostname + region
    try:
        ipv4Address = socket.getaddrinfo(fqdn,0,0,0,0)[0][4][0]
        return {'fqdn': socket.getfqdn(ipv4Address).upper(), 'ip': ipv4Address}
    except:
        if len(domainsList):
            return getFQDNAndIPAddress(hostname, domainsList)
        return {'fqdn': hostname.upper(), 'ip': False}

def commitAndPushInventory(gitUsername, gitPassword):
    gitUsername = gitUsername.split('\\')[-1]
    gitPassword = gitPassword.replace('$', '\\$')
    currentDirectory = os.getcwd()
    try:
        os.chdir('/tmp/GapTool/Ansible_Remediation')
        print(os.getcwd())
        print('PUSHING HOSTS FILE')
        os.system('git reset --hard')
        os.system('git pull https://' + gitUsername + ':' + gitPassword + '@gitserver.xtonet.com/TAM/Ansible_Remediation.git > /dev/null 2>&1')
        os.system('mv ../hosts hosts')
        os.system('git add hosts')
        os.system('git commit -m "Update hosts file from lalvartool"')
        os.system('git push https://' + gitUsername + ':' + gitPassword + '@gitserver.xtonet.com/TAM/Ansible_Remediation.git > /dev/null 2>&1')
        print("PUSH OK")
        return True
    except Exception as e:
        print(str(e))
        return False
    finally:
        os.chdir(currentDirectory)

def get_denounces():
    currentDirectory = os.getcwd()
    #dir = os.chdir('./tam_api')
    try:
        dir = os.chdir('./tam_api')

    except:
        os.system('git clone git@gitserver.xtonet.com:TAM/tam_api.git')
        dir = os.chdir('./tam_api')

    try:
        file_obj = open('quotes.txt', 'r')
        text = file_obj.read()
        quotes = text.splitlines()
        file_obj.close()
        for report in quotes:
            print(report)

    except Exception as e:
        print(str(e))
        return False

def checkGit():
    try:
        os.system('git --version')
        print("GIT OK")
        return True
    except Exception as e:
        print(str(e))
        print("Git isn't installed")
        return False

def funny_quotes():
    dir = os.chdir('./tam_api')
    file_obj = open('quotes.txt', 'r')
    text = file_obj.read()
    text = text.strip().strip()
    return [text]

#deviceList = queue.Queue()
server = 'itdwdb.na.xom.com'
#asd = getDevicesSQL(deviceList, server, True)
#get_denounces()
