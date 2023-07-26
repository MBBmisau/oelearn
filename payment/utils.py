#from .models import Order
from academic.utils import get_current_batch
from .models import Invoice, InvoicePaymentReferrence

#def get_order(user, product, batch):
#    order = Order.objects.filter(user=user,product=product,batch=batch).first()
#    if order is None:
#        order = Order.objects.create(user=user,product=product,batch=batch)
#    return order

def get_invoice(course, plan, student, batch):
    try:
        invoice = Invoice.objects.get(course=course,plan=plan,student=student,batch=batch)
    except Exception as e:
        invoice = Invoice.objects.create(course=course,plan=plan,student=student,batch=batch)
    return invoice

def get_ref(invoice):
    invoices = InvoicePaymentReferrence.objects.filter(invoice=invoice,is_used=False)
    if len(invoices) > 0:
        return invoices[:0]
    invoice = InvoicePaymentReferrence.objects.create(invoice=invoice)
    return invoice
