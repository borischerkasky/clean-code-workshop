from services.customer_plan import CustomerPlan
from services.email_service import EmailService
from services.crm import CRM

class Bank:
    def __init__(self):
        self.accounts = []
        pass

    @staticmethod
    def default_response():
        result = dict()
        result['warnings'] = []
        result['response'] = 'OK'

    # non information
    def move(self, yid, xid, how_much):
        response = self.default_response

        # Command query separation
        for a1 in self.accounts:
            if a1['id'] == xid:
                commission = self.calculate_commission(a1, how_much)
                a1['amount'] -= (commission + how_much)
                # boolean conditions as methods
                if a1['amount'] < a1['balance-warning-level'] and a1['balance-warning-enabled']:
                    response['Warnings'].append('balance is closing to zero!!!')
                a1['operations'] += 1
                self.accounts['bank-commissions'] += commission

                for a2 in self.accounts:
                    if a2['id'] == yid:
                        a2['amount'] += how_much

    # This method calculates the plan details for potential new Bank customers
    # Bank holds all plans in files on disk
    def plan_estimation(self, customer_name, expected_household_income):
        # Be a newspaper
        plan_file_name = self.get_plan_file(expected_household_income)
        file = open(plan_file_name, "r")
        lines = file.readlines()
        file.close()

        # variables can tell a story
        plan = CustomerPlan(lines[0], lines[1], lines[2], lines[3])

        # compact switch cases
        if plan.name == "VIP":
            EmailService.send_email("manager@bank.co.il", "potential revenue")
            EmailService.send_email("manager@bank.co.il", "customer welcome email")
            CRM.save_client_details(customer_name, expected_household_income)
            CRM.set_followup_reminder(customer_name, "manager")
        elif plan.name == 'Premium':
            EmailService.send_email("manager@bank.co.il", "customer welcome email")
            CRM.set_followup_reminder(customer_name, "account manager")

        return plan

    @staticmethod
    def get_plan_file(expected_income):
        if expected_income > 100000:
            return "vip.txt"
        elif expected_income > 10000:
            return "premium.txt"
        elif expected_income > 5000:
            return "basic.txt"
        else:
            return "default.txt"

    def how_much(self, xid):
        for a1 in self.accounts:
            if a1['id'] == xid:
                return a1['amount']

    def account_details(self, xid):
        for a1 in self.accounts:
            if a1['id'] == xid:
                return a1

    @staticmethod
    def calculate_commission(account, how_much):
        is_fixed_type = account['commission-settings']['type'] == 'fixed'
        # positive conditions
        if not is_fixed_type:
            value = account['commission-settings']['commission-value-percentage']
            if how_much < 1000:
                return value * how_much
            elif 1000 <= how_much < 10000:
                return 1.1 * value * how_much
            else:
                return 1.5 * value * how_much
        else:
            return account['commission-settings']['fixed-commission-value']
