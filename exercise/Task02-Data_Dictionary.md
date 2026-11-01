### Data Dictionary

#### categories

| Name          | Variable Description             | Data Type          | Unit of Measurement | Valid Values                                                                                            |
| ------------- | -------------------------------- | ------------------ | ------------------- | ------------------------------------------------------------------------------------------------------- |
| category_id   | Unique identifier of the category | Nominal categorical | Not applicable      | Unique identifiers: 1 to 8                                                                              |
| category_name | Name of the product category      | Nominal categorical | Not applicable      | Houseplants, Seeds & Bulbs, Tools, Pots & Planters, Soil & Compost, Watering, Fertilizer, Outdoor Decor |

#### customers

| Name        | Variable Description                          | Data Type                 | Unit of Measurement | Valid Values                                                |
| ----------- | --------------------------------------------- | ------------------------- | ------------------- | ----------------------------------------------------------- |
| customer_id | Unique identifier of the customer             | Nominal categorical        | Not applicable      | Unique identifiers: 1 to 20                                 |
| first_name  | Customer's first name                         | Nominal categorical        | Not applicable      | Non-empty text                                              |
| last_name   | Customer's last name                          | Nominal categorical        | Not applicable      | Non-empty text                                              |
| email       | Customer's email address                      | Nominal categorical        | Not applicable      | Email addresses in valid format                             |
| phone       | Customer's contact phone number               | Nominal categorical        | Not applicable      | Phone numbers in text format; may be missing                |
| city        | City of residence provided by the customer    | Nominal categorical        | Not applicable      | City names                                                  |
| state       | State of residence provided by the customer   | Nominal categorical        | State abbreviation  | U.S. state abbreviations                                    |
| signup_date | Customer's registration date                  | Date                       | Date                | Valid dates in YYYY-MM-DD format                            |
| is_active   | Indicates whether the customer account is active | Binary nominal categorical | Not applicable      | true (active), false (inactive)                             |

#### order_items

| Name          | Variable Description                                   | Data Type          | Unit of Measurement | Valid Values                                      |
| ------------- | ------------------------------------------------------ | ------------------ | ------------------- | ------------------------------------------------- |
| order_item_id | Unique identifier of the item recorded in the order    | Nominal categorical | Not applicable      | Unique identifiers: 1 to 48                       |
| order_id      | Identifier of the order to which the item belongs      | Nominal categorical | Not applicable      | Identifiers existing in orders.order_id           |
| product_id    | Identifier of the product purchased                    | Nominal categorical | Not applicable      | Identifiers existing in products.product_id       |
| quantity      | Number of units of the product in the order            | Discrete numeric    | Units               | Positive integers                                 |
| unit_price    | Unit price recorded for the product in the order       | Continuous numeric  | Dollars (USD)       | Non-negative monetary values                      |

#### orders

| Name         | Variable Description                             | Data Type          | Unit of Measurement | Valid Values                                            |
| ------------ | ------------------------------------------------ | ------------------ | ------------------- | ------------------------------------------------------- |
| order_id     | Unique identifier of the order                   | Nominal categorical | Not applicable      | Unique identifiers: 1 to 24                             |
| customer_id  | Identifier of the customer who placed the order  | Nominal categorical | Not applicable      | Identifiers existing in customers.customer_id           |
| order_date   | Date on which the order was placed               | Date                | Date                | Valid dates in DD/MM/YYYY format                        |
| shipped_date | Date on which the order was shipped to the customer | Date             | Date                | Valid dates in DD/MM/YYYY format; may be missing        |
| status       | Order status                                     | Nominal categorical | Not applicable      | shipped, pending, processing, cancelled                 |
| coupon_code  | Promotional code used on the order               | Nominal categorical | Not applicable      | Text codes; may be missing                              |

#### products

| Name             | Variable Description                                      | Data Type                  | Unit of Measurement | Valid Values                                         |
| ---------------- | --------------------------------------------------------- | -------------------------- | ------------------- | ---------------------------------------------------- |
| product_id       | Unique identifier of the product                          | Nominal categorical         | Not applicable      | Unique identifiers: 1 to 24                          |
| product_name     | Commercial name of the product                            | Nominal categorical         | Not applicable      | Non-empty text                                       |
| category_id      | Identifier of the product category                        | Nominal categorical         | Not applicable      | Identifiers existing in categories.category_id       |
| supplier_id      | Identifier of the supplier associated with the product    | Nominal categorical         | Not applicable      | Identifiers existing in suppliers.supplier_id        |
| price            | Current selling price of the product                      | Continuous numeric          | Dollars (USD)       | Non-negative monetary values                         |
| cost             | Unit cost recorded for the product                        | Continuous numeric          | Dollars (USD)       | Non-negative monetary values                         |
| quantity_on_hand | Number of units currently available in stock              | Discrete numeric            | Units               | Non-negative integers                                |
| reorder_level    | Stock level defined as the reference for replenishment   | Discrete numeric            | Units               | Non-negative integers                                |
| discontinued     | Indicates whether the product has been discontinued       | Binary nominal categorical  | Not applicable      | TRUE (discontinued), FALSE (not discontinued)        |

#### suppliers

| Name          | Variable Description                               | Data Type          | Unit of Measurement | Valid Values                                              |
| ------------- | -------------------------------------------------- | ------------------ | ------------------- | --------------------------------------------------------- |
| supplier_id   | Unique identifier of the supplier                  | Nominal categorical | Not applicable      | Unique identifiers: 1 to 6                                |
| supplier_name | Commercial name of the supplier                    | Nominal categorical | Not applicable      | Non-empty text                                            |
| contact_email | Email address for contacting the supplier          | Nominal categorical | Not applicable      | Email addresses in valid format; may be missing           |
| state         | State provided in the supplier's registration      | Nominal categorical | State abbreviation  | U.S. state abbreviations                                  |

