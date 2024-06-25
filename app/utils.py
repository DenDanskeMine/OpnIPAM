import asyncio
import logging
import ipaddress
import aioping
from app import db
from app.models import IPAddress

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ping_ip(ip_id):
    ip = IPAddress.query.get(ip_id)
    logger.info(f"Pinging IP: {ip.ip_address}")
    try:
        await aioping.ping(ip.ip_address, timeout=5)  # Use ICMP ping
        ip.is_active = True
        logger.info(f"Ping successful for {ip.ip_address}")
    except TimeoutError:
        ip.is_active = False
        logger.error(f"Ping failed for {ip.ip_address}")
    db.session.commit()

async def ping_subnet(subnet_id):
    logger.info(f"Starting subnet scan for subnet ID: {subnet_id}")
    ips = IPAddress.query.filter_by(subnet_id=subnet_id).all()
    tasks = [ping_ip(ip.id) for ip in ips]
    await asyncio.gather(*tasks)
    logger.info(f"Completed subnet scan for subnet ID: {subnet_id}")

async def discover_ips(cidr, subnet_id):
    logger.info(f"Starting IP discovery for CIDR: {cidr}")
    network = ipaddress.ip_network(cidr)
    tasks = []
    for ip in network.hosts():
        task = asyncio.ensure_future(ping_and_add_ip(str(ip), subnet_id))
        tasks.append(task)
    await asyncio.gather(*tasks)
    logger.info(f"Completed IP discovery for CIDR: {cidr}")

async def ping_and_add_ip(ip_address, subnet_id):
    try:
        await aioping.ping(ip_address, timeout=5)  # Use ICMP ping
        logger.info(f"Discovered active IP: {ip_address}")
        existing_ip = IPAddress.query.filter_by(ip_address=ip_address, subnet_id=subnet_id).first()
        if not existing_ip:
            ip = IPAddress(ip_address=ip_address, subnet_id=subnet_id, is_active=True)
            db.session.add(ip)
            db.session.commit()
    except TimeoutError:
        logger.error(f"Ping failed for {ip_address}")
