import sys
sys.path.append('./Model')
from price_predictions_in_ecommercewish import PriceModel
from sales_predictions_in_ecommercewish import SalesModel


if __name__ == "__main__":
    priceModel = PriceModel()
    priceModel.execute()
    salesModel = SalesModel()
    salesModel.execute()