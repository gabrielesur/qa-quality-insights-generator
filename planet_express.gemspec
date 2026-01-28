# frozen_string_literal: true

require_relative 'lib/planet_express/version'

Gem::Specification.new do |spec|
  spec.name          = 'planet_express'
  spec.version       = PlanetExpress::VERSION
  spec.authors       = ['Philip J. Fry']
  spec.email         = ['philip@planetexpress.com']

  spec.summary       = 'Calculate your shipment discounts easily'
  spec.description   = 'A library to calculate the applicable shipment discounts for a list of shipments.'
  spec.homepage      = 'https://github.com/timkaechele/planet_express'
  spec.license       = 'MIT'
  spec.required_ruby_version = Gem::Requirement.new('>= 2.4.0')

  # spec.metadata["allowed_push_host"] = "TODO: Set to 'http://mygemserver.com'"

  spec.metadata['homepage_uri'] = spec.homepage
  # spec.metadata["source_code_uri"] = "TODO: Put your gem's public repo URL here."
  # spec.metadata["changelog_uri"] = "TODO: Put your gem's CHANGELOG.md URL here."

  # Specify which files should be added to the gem when it is released.
  # The `git ls-files -z` loads the files in the RubyGem that have been added into git.
  spec.files = Dir.chdir(File.expand_path(__dir__)) do
    `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  end
  spec.bindir        = 'exe'
  spec.executables   = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
  spec.require_paths = ['lib']

  spec.add_development_dependency('factory_bot', '~> 6.1')
  spec.add_development_dependency('rubocop', '~> 1.11')
  spec.add_development_dependency('simplecov', '~> 0.21')
end
