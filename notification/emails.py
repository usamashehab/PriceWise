from templated_mail.mail import BaseEmailMessage


class PriceAlert(BaseEmailMessage):
    template_name = "email/price_alert.html"
