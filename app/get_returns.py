from app import app, db

def tax(cr):
    income,tax=0, 0
    for t in cr:
    	income+=t.amount
   
    if income < 250000:
    	return tax, income
    elif income < 500000:
    	tax = income/20
    	return tax, income
    elif income < 750000:
    	return income/10, income
    elif income < 1000000:
        return 15*(income/100), income
    elif income < 1250000:
    	return 20*(income/100), income
    elif income < 1500000:
    	return 25*(income/100), income
    else:
    	return 30*(income/100), income		    	
