def calcualte_monthly_payment(M0, c, n):
    """
    calcualte monthly payment
    :param M0: Total loan amount
    :param c: Annual coupon rate
    :param n: total payment months
    :return: monthly payment
    """
    c = c / 12
    compound_rate = (1 + c) ** n
    B = M0 * c * compound_rate / (compound_rate - 1)
    return B


def calculate_WAC(c, balances):
    """
    calculate pool weighted average coupon (WAC)
    :param c: annual coupon rate
    :param balances: loan balances
    :return: pool WAC
    """
    c = c / 12
    total_balance = sum(balances)
    if int(total_balance) == 0:
        return 0
    total_payment = 0
    for i, balance in enumerate(balances):
        total_payment += balance * c
    return round(total_payment / total_balance * 12 ,5)

def calculate_WAL(all_principal_payments_list, all_balances_list, k, unit = 'year'):
    """
    calculate pool weighted average life (WAL)
    :param all_principal_payments_list: a list of principal payments for each loan from 0 to n (0 is the first principal payment)
    :param all_balances_list: a list of balances for each loan from 0 to n (principal balance at time 0 is the original loan amount)
    :param k:
    :return: WAL pool
    """
    numerator = 0
    denominator = 0
    for l in range(len(all_principal_payments_list)):
        all_principal_payments = all_principal_payments_list[l]
        all_balances = all_balances_list[l]
        for time in range(k+1, len(all_principal_payments)):
            numerator += (time - k) * all_principal_payments[time]
        denominator += all_balances[k]
    if denominator == 0:
        return 0
    if unit == 'year':
        return round(numerator / denominator / 12, 4)
    return round(numerator / denominator, 4)


# class MBS:
#     def __init__(self, principal: float, WAC: float, year: int, psa: float):
#         self.principal = principal
#         self.WAC = WAC
#         self.year = year
#         self.psa: PSA | None = None
#         self.set_psa(psa)
#
#     def set_psa(self, speed):
#         self.psa: PSA = PSA(speed)
#
#     def calculate_cashflows(self):
#         balance = self.principal
#         i = 0
#         balances = [balance]
#         interest_expenses = [0]
#         scheduled_principal_payments = [0]
#         unscheduled_principal_payments = [0]
#         month_indices = [i]
#
#         scheduled_payment = calcualte_monthly_payment(self.principal, self.WAC, self.year * 12)
#
#         while balance > 0:
#             i += 1
#             month_indices.append(i)
#             interest_payment = cal_monthly_interest_payment(balance, WAC)
#             scheduled_principal_payment = scheduled_payment - interest_payment
#             if balance < scheduled_principal_payment:
#                 scheduled_principal_payment = balance
#                 actual_balance = 0
#                 unscheduled_principal_payment = 0
#             else:
#                 smm = self.psa.SMM(i)
#                 prepayment = cal_prepayment(scheduled_balance=balance - scheduled_principal_payment, smm=smm)
#                 unscheduled_principal_payment = prepayment
#                 actual_balance = cal_actual_balance(previous_balance=balance,
#                                                     scheduled_principal_payment=scheduled_principal_payment,
#                                                     prepayment=prepayment)
#
#             balance = actual_balance
#             balances.append(balance)
#             interest_expenses.append(interest_payment)
#             scheduled_principal_payments.append(scheduled_principal_payment)
#             unscheduled_principal_payments.append(unscheduled_principal_payment)
#
#         cashflows = pd.DataFrame({
#             "Month": month_indices[1:],
#             "Beginning Balance": balances[:-1],
#             "Scheduled Principal Payments": scheduled_principal_payments[1:],
#             "Unscheduled Principal Payments": unscheduled_principal_payments[1:],
#             "Interest Expense": interest_expenses[1:],
#             "Unpaid Balance": balances[1:],
#             "Paid Principal": [self.principal - x for x in balances[1:]]
#         })
#
#         cashflows.set_index("Month", inplace=True)
#
#         return cashflows