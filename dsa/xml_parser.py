import xml.etree.ElementTree as ET
import re

def xmlParsing(xml_file):

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        print(root.tag)
        print(len(root))

        record = []

        for sms in root.iter('sms'):
            body = sms.get("body", "")
            timestamp = sms.get("readable_date", "")
            idFind = re.search(r'(?:TxId:|Financial Transaction Id:)\s*(\d+)', body)
            tx_id = idFind.group(1) if idFind else "N/A"
            amountFind = re.search(r'([\d,]+)\s*RWF', body)
            amount = amountFind.group(1).replace(',', '') if amountFind else 0

            if "received" in body:
                transactionType = "Transfer Received"
                senderFind = re.search(r'from\s+(.*?)\s+\(', body)
                sender = senderFind.group(1) if senderFind else "Unknown"
                receiver = "Mobile Money User"
            elif "payment" in body:
                transactionType = "Payment"
                sender = "Mobile Money User"
                receiverFind = re.search(r'to\s+(.*?)\s+(?:\d|has)', body)
                receiver = receiverFind.group(1).strip() if receiverFind else "MTN"
            elif "deposit" in body:
                transactionType = "Bank Deposit"
                sender = "Bank System"
                receiver = "Mobile Money User"
            else:
                transactionType = "Other"
                sender = "System"
                receiver = "System"

            record.append({
                "id": tx_id,
                "type": transactionType,
                "amount": amount,
                "sender": sender,
                "receiver": receiver,
                "timestamp": timestamp
            })

        return [r for r in record if r['id'] != "N/A"]

    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []
