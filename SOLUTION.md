# Solution *"Planet Express"*

*Planet Express* is a gem for calculating discounts for your shipments based on a given rule set and an available
discount budget.

## Installation

Get the source code from GitHub and run `bundle install`.

We recommend ruby 2.6.6 or MRI 2.7 to run the code. Other ruby versions should work, but are not officially supported.

## Usage

The sample input file is written to adhere to the following format:

```
# ISO8601Date PackageSize Provider
2015-02-01 S PR
```

Now that you have an input file like that you can run the processing with the following rake task. There is a sample
'input.txt' file in project root folder for you:

```sh
$ bundle exec rake 'process[path/to/input.txt]'

# 2015-02-01 S MR 1.50 0.50
# 2015-02-02 S MR 1.50 0.50
# 2015-02-03 L LP 6.90 -
# 2015-02-05 S LP 1.50 -
# 2015-02-06 S MR 1.50 0.50
# 2015-02-06 L LP 6.90 -
# 2015-02-07 L MR 4.00 -
# 2015-02-08 M MR 3.00 -
# 2015-02-09 L LP 0.00 6.90
# 2015-02-10 L LP 6.90 -
# 2015-02-10 S MR 1.50 0.50
# 2015-02-10 S MR 1.50 0.50
# 2015-02-11 L LP 6.90 -
# 2015-02-12 M MR 3.00 -
# 2015-02-13 M LP 4.90 -
# 2015-02-15 S MR 1.50 0.50
# 2015-02-17 L LP 6.90 -
# 2015-02-17 S MR 1.90 0.10
# 2015-02-24 L LP 6.90 -
# 2015-03-01 S MR 1.50 0.50
```

## Design Decisions

The program is divided into four core modules:

- **Discounts** - provides a class to represent discounts as well as a budget to keep track of the discount budgets for
  a given month.
- **Shipments** - a basic representation of a shipment as in "an order that will be shipped".
- **ShippingOptions** - a structure and a repository to represent providers and their shipping options.
- **Rules** - contains all the logic for discount rules including a methods to apply discounts to shipments.

### Discounts

The discount class represents a discount that originated from a discount rule and contains the monetary amount as well
as the rule that is responsible for applying the discount.

Use the `DiscountBudgetForMonthRepository` to get the discount budget for a given month.

### Shipments

Shipments are the input for all calculation and have a date and a reference to a shipping option. They also keep track
of discounts applied to them.

To provide structured output, you can use the `ShipmentFormatter` which formats  a given `Shipment` as a
whitespace-separated CSV.

### Shipping Options

Shipping option is a structure to represent an individual shipping option, it  includes the price, the provider as well
as the package size.

Use the `ShippingOptionRepository` to retrieve shipping options and to query specific providers or package sizes.

### ShipmentDiscountCalculator

This class is the entry point for calculating discounts for a list of shipments. It takes a`shipment_repository` and a
list of rules and applies the list of rules to the given shipments

Example:

```ruby
calculator = ShipmentDiscountCalculator.new(
  shipment_repository: ShipmentRepository.new(data: []),
  shipping_option_repository: ShippingOptionRepository.new,
  rules: [Rule.new(...)],
  input: File.open('input.txt', 'r')
)

calculator.run([Shipment.new])
```

### Repository

The repository base class is the managing unit to retrieve and store shared state. When possible nobody should query the
data directly, but define a query method in the repository to retrieve the required data.

It provides an ActiveRecord like `where` method with which you can query for multiple attributes in one call:

```ruby
repo.where(attribute_a: 5, attribute_b: 'Test')
```

## Development

After checking out the repo, run `bin/setup` to install dependencies. Then run `rake spec` to run the tests. You can
also run `bin/console` for an interactive prompt that will allow you to experiment.

To install this gem onto your local machine, run `bundle exec rake install`.
