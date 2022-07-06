from flask import *
import sqlite3
from ccplatform import CreateNewVIrtualMachine
from ccplatform import getIPaddress
#from ip import getParts
from ip import get_url
import time

def get_db_connection():
    conn = sqlite3.connect('db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
query = 'SELECT users.name as vmowner, vms.vmname, vms.Memory as ram, states.state, cpu.cpuname, cpu.speed, OPeratingSystems.OS_name, OPeratingSystems.OS_platform, OPeratingSystems.OS_codename, OPeratingSystems.OS_family, OPeratingSystems.OS_version, OPeratingSystems.OS_variant, OPeratingSystems.OS_sourcemodel, OPeratingSystems.Kernel FROM vms JOIN users ON vms.vmowner = users.id JOIN OPeratingSystems ON vms.os = OPeratingSystems.id JOIN states ON vms.vmstate = states.id JOIN cpu ON vms.cpu = cpu.id'
vmquery = conn.execute(query).fetchall()

cpu = conn.execute('SELECT * FROM cpu').fetchall()

opsys = conn.execute('SELECT * FROM OPeratingSystems').fetchall()


opsys_disk = conn.execute('SELECT OS_disk FROM OPeratingSystems WHERE id = 4').fetchall()
print(opsys_disk[0]['OS_disk'])
#print(vmquery[1]['OS_codename'])




app = Flask(__name__)

@app.route('/vms')
def index():

    return render_template('index.html', vmquery=vmquery)
    
@app.route('/ip')
def ip():
    #getIPaddress()
    #time.sleep(10)
    #ssh = get_url(getIPaddress())
    return render_template('ip.html', vmquery=vmquery)

# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':

        title = request.form['os']
        ram = request.form['memory']
        user = request.form['user']
        cpuname = request.form['cpu']
        vmname = request.form['vmname']
        cores = request.form['cores']
        
        fetcher = get_db_connection()

        os = fetcher.execute('SELECT * FROM OPeratingSystems').fetchall()
        os_val = 0
        cpu_id = 0

        for x in os:
            if title == x['Os_name']:
                os_val = x['id']

        cpu_fetch = fetcher.execute('SELECT * FROM cpu').fetchall()
        for processor_id in cpu_fetch:
            if request.form['cpu'] ==  processor_id['cpuname']:
                cpu_id = processor_id['id']
                 
        if not title:
            flash('Title is required!')
       
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO vms (vmname, vmowner, vmstate, os, Memory, cpu, cores) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (vmname, user, '7', os_val , ram, cpu_id, cores,))
            conn.commit()
            CreateNewVIrtualMachine(vmname, ram, cores)
            conn.close()
            return redirect(url_for('index'))
       

    return render_template('create.html', cpu=cpu, opsys=opsys)
if __name__== '__main__':
    app.run(debug=True, port=5000)

conn.close()