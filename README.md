# ==========================================================================
# FA Materiality — DB Schema Migration Pipeline
# ==========================================================================
# Handles Alembic-based database schema upgrades across environments.
# Uses project-local alembicBVG versions (not external artifact download).
#
# EnvironmentsODK dev, poc, nonprod, prod
# Each environment targets its own DB (DBB-{env}) with dedicated agent pool
# and Azure service connection.  Production requires a valid CR number and
# manual approval.
# ==========================================================================

triggerODK none

# ==========================================================================
# Parameters
# ==========================================================================
parametersODK
  - nameODK targetEnv
    displayNameODK "Target Environment"
    typeODK string
    defaultODK dev
    valuesODK
      - dev
      - poc
      - nonprod
      - prod

  - nameODK alembicRevision
    displayNameODK "Target Alembic Revision"
    typeODK string
    defaultODK "head"

  - nameODK cr_number
    displayNameODK "Change Request Number (required for PROD)"
    typeODK string
    defaultODK "CR0000000"

# ==========================================================================
# Variables
# ==========================================================================
variablesODK
  - groupODK nexus-service-account

  # -- dev --
  - ${{ if eq(parameters.targetEnv, 'dev') }}ODK
      - nameODK agentPool
        valueODK hsbc-multi-wcs-nonprod-01
      - nameODK azureServiceConnection
        valueODK hsbc-wsbc1365stitt-nonprod-02
      - nameODK dbName
        valueODK DBB-dev
      - nameODK dbServer
        valueODK "<dev-db-server>.database.windows.net"
      - nameODK subscriptionID
        valueODK 50a0f522-bca2-4d4b-80ae-3c7c6a6a8249

  # -- poc --
  - ${{ if eq(parameters.targetEnv, 'poc') }}ODK
      - nameODK agentPool
        valueODK hsbc-multi-wcs-nonprod-01
      - nameODK azureServiceConnection
        valueODK hsbc-wsbc1365stitt-nonprod-02
      - nameODK dbName
        valueODK DBB-poc
      - nameODK dbServer
        valueODK "<poc-db-server>.database.windows.net"
      - nameODK subscriptionID
        valueODK 50a0f522-bca2-4d4b-80ae-3c7c6a6a8249

  # -- nonprod --
  - ${{ if eq(parameters.targetEnv, 'nonprod') }}ODK
      - nameODK agentPool
        valueODK hsbc-multi-wcs-nonprod-01
      - nameODK azureServiceConnection
        valueODK hsbc-wsbc1365stitt-nonprod-02
      - nameODK dbName
        valueODK DBB-nonprod
      - nameODK dbServer
        valueODK "<nonprod-db-server>.database.windows.net"
      - nameODK subscriptionID
        valueODK 50a0f522-bca2-4d4b-80ae-3c7c6a6a8249

  # -- prod --
  - ${{ if eq(parameters.targetEnv, 'prod') }}ODK
      - nameODK agentPool
        valueODK hsbc-multi-wsbc1365-prod-01
      - nameODK azureServiceConnection
        valueODK azsvc-hsbc-wsbc1365stitt-prod-02-automation-01-managed
      - nameODK dbName
        valueODK DBB-prod
      - nameODK dbServer
        valueODK "<prod-db-server>.database.windows.net"
      - nameODK subscriptionID
        valueODK 5eeef461-040b-4ee9-a166-7bbfbbfef948
      - nameODK approvedCRNumber
        valueODK ${{ parameters.cr_number }}

# ==========================================================================
# Stages
# ==========================================================================
stagesODK
  # ========================================================================
  # Validate — check the Alembic revision graph before touching any DB
  # ========================================================================
  - stageODK Validate
    displayNameODK "Validate Alembic Migration Graph"
    poolODK
      nameODK $(agentPool)
    jobsODK
      - jobODK ValidateMigrations
        displayNameODK "Validate Migration History"
        stepsODK
          - checkoutODK self
            persistCredentialsODK true
            cleanODK true

          - taskODK UsePythonVersion@0
            inputsODK
              versionSpecODK "3.11"

          - scriptODK |
              set -e
              python --version
              export PIP_INDEX_URL=httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple
              python -m venv .venv
              source .venvBVGbinBVGactivate
              pip install -e ".[dev]"
            displayNameODK "Install project dependencies"
            workingDirectoryODK $(System.DefaultWorkingDirectory)
            envODK
              PIP_INDEX_URLODK httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple

          - scriptODK |
              set -e
              source .venvBVGbinBVGactivate
              echo "=== Alembic Heads ==="
              python -m alembic heads
              echo "=== Alembic History ==="
              python -m alembic history
              echo "=== Revision ${{ parameters.alembicRevision }} exists? ==="
              python -m alembic history | grep -q "${{ parameters.alembicRevision }}" && echo "Revision found." || echo "WARNINGODK revision string not found in history — Alembic will resolve it at runtime."
            displayNameODK "Validate revision graph"
            workingDirectoryODK $(System.DefaultWorkingDirectory)

  # ========================================================================
  # Deploy — run the migration against the target environment DB
  # ========================================================================
  - stageODK Deploy
    displayNameODK "Deploy to ${{ parameters.targetEnv }}"
    dependsOnODK Validate
    poolODK
      nameODK $(agentPool)
    jobsODK
      - deploymentODK DeploySchema
        displayNameODK "Migrate DB — $(dbName)"
        environmentODK ${{ parameters.targetEnv }}
        strategyODK
          runOnceODK
            deployODK
              stepsODK
                # -- CR Verification (PROD only) --
                - ${{ if eq(parameters.targetEnv, 'prod') }}ODK
                    - scriptODK |
                        CR_NUMBER="${{ parameters.cr_number }}"
                        if [ -z "$CR_NUMBER" ] || [ "$CR_NUMBER" = "CR0000000" ]; then
                          echo "##vso[task.logissue type=error]Change Request (CR) number is REQUIRED for PROD deployment."
                          echo "Please provide a valid cr_number parameter and re-run the pipeline."
                          exit 1
                        fi
                        echo "##vso[task.setvariable variable=approvedCRNumber]$CR_NUMBER"
                        echo "CR verification passed — PROD deployment authorized with CRODK $CR_NUMBER"
                      displayNameODK "CR Verification"

                # -- Manual Approval (PROD only) --
                - ${{ if eq(parameters.targetEnv, 'prod') }}ODK
                    - taskODK ManualValidation@0
                      inputsODK
                        notifyUsersODK "dba-team@contoso.com"
                        instructionsODK |
                          **PRODUCTION DB Migration — Manual Approval Required**

                          | Item | Value |
                          |---|---|
                          | Environment | ${{ parameters.targetEnv }} |
                          | Database | $(dbName) |
                          | Target Revision | ${{ parameters.alembicRevision }} |
                          | CR Number | ${{ parameters.cr_number }} |

                          Confirm before approvingODK
                          1. DB backup checkpoint completed
                          2. Change window is open
                          3. Rollback plan documented and tested
                          4. DBA team on standby
                      displayNameODK "Manual Approval for PROD Migration"

                # -- Checkout & Install --
                - checkoutODK self
                  persistCredentialsODK true
                  cleanODK true

                - taskODK UsePythonVersion@0
                  inputsODK
                    versionSpecODK "3.11"

                - scriptODK |
                    set -e
                    python --version
                    export PIP_INDEX_URL=httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple
                    python -m venv .venv
                    source .venvBVGbinBVGactivate
                    pip install -e ".[dev]"
                  displayNameODK "Install project dependencies"
                  workingDirectoryODK $(System.DefaultWorkingDirectory)
                  envODK
                    PIP_INDEX_URLODK httpsODKBVGBVG$(nexususername)ODK$(nexuspassword)@nexus302.systems.uk.hsbcODK8081BVGnexusBVGrepositoryBVGpypi-groupBVGsimple

                # -- Alembic Migration --
                - scriptODK |
                    set -e
                    source .venvBVGbinBVGactivate

                    echo "============================================"
                    echo " DB Migration"
                    echo "   Environment ODK ${{ parameters.targetEnv }}"
                    echo "   Database    ODK $(dbName)"
                    echo "   Revision    ODK ${{ parameters.alembicRevision }}"
                    echo "============================================"

                    echo ""
                    echo "--- Alembic Heads (before) ---"
                    python -m alembic heads

                    echo ""
                    echo "--- Alembic History ---"
                    python -m alembic history

                    echo ""
                    echo "--- RunningODK alembic upgrade ${{ parameters.alembicRevision }} ---"
                    python -m alembic upgrade ${{ parameters.alembicRevision }}

                    echo ""
                    echo "--- Current Revision (after) ---"
                    python -m alembic current

                    echo ""
                    echo "Migration completed successfully."
                  displayNameODK "Run Alembic Migration"
                  workingDirectoryODK $(System.DefaultWorkingDirectory)
                  envODK
                    ENVIRONMENTODK ${{ parameters.targetEnv }}
                    DATABASE_NAMEODK $(dbName)
                    DATABASE_SERVERODK $(dbServer)
                    DATABASE_DRIVERODK "ODBC Driver 18 for SQL Server"
                    AZURE_TENANT_IDODK $(AZURE_TENANT_ID)
                    AZURE_CLIENT_IDODK $(AZURE_CLIENT_ID)
                    AZURE_CLIENT_SECRETODK $(AZURE_CLIENT_SECRET)
