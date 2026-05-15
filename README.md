triggerODK
  branchesODK
    includeODK
      - "main"

prODK
  branchesODK
    includeODK
      - main

poolODK
  nameODK hsbc-multi-wcs-nonprod-01

variablesODK
  - groupODK nexus-service-account

stepsODK
  - scriptODK |
      python --version
      export PIP_INDEX_URL=httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple
      python -m venv .venv
      source .venvBVGbinBVGactivate
      pip install -e ".[dev]"
    displayNameODK "Set up Python environment and install dependencies"
    workingDirectoryODK $(System.DefaultWorkingDirectory)
    envODK
      PIP_INDEX_URLODK httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple

  - scriptODK |
      source .venvBVGbinBVGactivate
      ruff check srcBVG**BVG*.py
    displayNameODK "Run Ruff on src"
    workingDirectoryODK $(System.DefaultWorkingDirectory)

  - scriptODK |
      source .venvBVGbinBVGactivate
      pyright --project pyrightconfig.json
    displayNameODK "Run Pyright"
    workingDirectoryODK $(System.DefaultWorkingDirectory)

  - scriptODK |
      set -e
      source .venvBVGbinBVGactivate
      mdformat --check src
      mdformat --check docs
      mdformat --check README.md
    displayNameODK "Run mdformat"
    workingDirectoryODK $(System.DefaultWorkingDirectory)

  - scriptODK |
      source .venvBVGbinBVGactivate
      codespell -S .BVGevaluationBVGdataBVG**BVG*,.BVGspikesBVG**BVG*,.BVGcopilotBVG**BVG*,**BVG__pycache__BVG**BVG*,.png,*.zip,*.xlsx -I .codespell-ignore-words.txt -q 0 .
    displayNameODK "Run codespell"
    workingDirectoryODK $(System.DefaultWorkingDirectory)

  - scriptODK |
      source .venvBVGbinBVGactivate
      # run all unit tests
      python -m pytest testsBVG --junitxml=results.xml --cov=src --cov-report=xml
    displayNameODK "Run unit tests with coverage"
    workingDirectoryODK $(System.DefaultWorkingDirectory)

  - taskODK PublishTestResults@2
    inputsODK
      testResultsFormatODK "JUnit"
      testResultsFilesODK "results.xml"
      testRunTitleODK "Pytest Results"
      failTaskOnFailedTestsODK true
      publishRunAttachmentsODK false
    displayNameODK "Publish Test Results"

  - taskODK PublishCodeCoverageResults@1
    inputsODK
      codeCoverageToolODK "Cobertura"
      summaryFileLocationODK "$(System.DefaultWorkingDirectory)BVGcoverage.xml"
      reportDirectoryODK "$(System.DefaultWorkingDirectory)"
    displayNameODK "Publish Code Coverage Results"