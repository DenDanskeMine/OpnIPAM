import asyncio
from flask import render_template, redirect, url_for, request, jsonify, flash
from app import app, db
from app.models import Subnet, IPAddress
from app.utils import ping_ip, ping_subnet, discover_ips
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    subnets = Subnet.query.filter_by(parent_id=None).all()
    return render_template('dashboard.html', title='Dashboard', subnets=subnets)

@app.route('/subnet/<int:subnet_id>')
def view_subnet(subnet_id):
    subnet = Subnet.query.get_or_404(subnet_id)
    ips = IPAddress.query.filter_by(subnet_id=subnet_id).all()
    return render_template('subnet.html', title=f'Subnet {subnet.cidr}', subnet=subnet, ips=ips)

@app.route('/add_subnet', methods=['GET', 'POST'])
def add_subnet():
    if request.method == 'POST':
        name = request.form['name']
        cidr = request.form['cidr']
        description = request.form['description']
        parent_id = request.form.get('parent_id')
        new_subnet = Subnet(name=name, cidr=cidr, description=description, parent_id=parent_id)
        db.session.add(new_subnet)
        db.session.commit()
        return redirect(url_for('index'))
    subnets = Subnet.query.all()
    return render_template('add_subnet.html', title='Add Subnet', subnets=subnets)

@app.route('/add_ip', methods=['GET', 'POST'])
def add_ip():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        description = request.form['description']
        subnet_id = request.form['subnet_id']
        new_ip = IPAddress(ip_address=ip_address, description=description, subnet_id=subnet_id)
        db.session.add(new_ip)
        db.session.commit()
        return redirect(url_for('index'))
    subnets = Subnet.query.all()
    return render_template('add_ip.html', title='Add IP Address', subnets=subnets)

@app.route('/edit_ip/<int:ip_id>', methods=['GET', 'POST'])
def edit_ip(ip_id):
    ip = IPAddress.query.get_or_404(ip_id)
    if request.method == 'POST':
        try:
            ip.ip_address = request.form['ip_address']
            ip.description = request.form['description']
            ip.is_active = 'is_active' in request.form
            ip.hostname = request.form['hostname']
            ip.mac_address = request.form['mac_address']
            ip.rack = request.form['rack']
            ip.device = request.form['device']
            ip.port = request.form['port']
            ip.os = request.form['os']
            ip.last_user = request.form['last_user']
            db.session.commit()
            flash('IP address updated successfully!', 'success')
            return redirect(url_for('view_subnet', subnet_id=ip.subnet_id))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update IP: {e}")
            flash('Failed to update IP address.', 'danger')
            return render_template('edit_ip.html', title='Edit IP', ip=ip), 400
    return render_template('edit_ip.html', title='Edit IP', ip=ip)

@app.route('/ping_ip/<int:ip_id>')
async def ping_ip_view(ip_id):
    logger.info(f"Ping IP view called for IP ID: {ip_id}")
    await ping_ip(ip_id)
    return jsonify({'status': 'Completed'})

@app.route('/ping_subnet/<int:subnet_id>')
async def ping_subnet_view(subnet_id):
    logger.info(f"Ping subnet view called for subnet ID: {subnet_id}")
    await ping_subnet(subnet_id)
    return jsonify({'status': 'Completed'})

@app.route('/discover_ips/<int:subnet_id>')
async def discover_ips_view(subnet_id):
    logger.info(f"Discover IPs view called for subnet ID: {subnet_id}")
    subnet = Subnet.query.get_or_404(subnet_id)
    await discover_ips(subnet.cidr, subnet_id)
    return jsonify({'status': 'Completed'})
