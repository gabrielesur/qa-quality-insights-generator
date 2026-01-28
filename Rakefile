# frozen_string_literal: true

require 'bundler/gem_tasks'
require 'rspec/core/rake_task'
require 'planet_express'

RSpec::Core::RakeTask.new(:spec)

task default: :spec

task :process, [:input_file] do |_t, args|
  file = File.open(args.input_file, 'r')

  shipping_option_repository = PlanetExpress::ShippingOptionRepository.new
  shipment_repository = PlanetExpress::ShipmentRepository.new(data: [])
  discount_budget_for_month_repository = PlanetExpress::DiscountBudgetForMonthRepository.new

  shipment_formatter = PlanetExpress::ShipmentFormatter.new

  rules = [
    PlanetExpress::SShipmentDiscountRule.new(
      discount_budget_for_month_repository: discount_budget_for_month_repository,
      shipping_option_repository: shipping_option_repository,
      shipment_repository: shipment_repository
    ),
    PlanetExpress::LShipmentDiscountRule.new(
      discount_budget_for_month_repository: discount_budget_for_month_repository,
      shipping_option_repository: shipping_option_repository,
      shipment_repository: shipment_repository
    )
  ]

  PlanetExpress::ShipmentDiscountCalculator.new(
    shipment_repository: shipment_repository,
    shipping_option_repository: shipping_option_repository,
    rules: rules,
    input: file
  ).run

  shipment_repository.each do |shipment|
    puts shipment_formatter.format(shipment)
  end
end
