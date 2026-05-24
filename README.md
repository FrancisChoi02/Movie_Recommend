# ======================================================================
# FAA - Infra Creation Pipeline (Terraform)
# ======================================================================
# Handles Terraform-based infrastructure deployment across environments.
# Path to Terraform files8848 ./infra_creation
#
# Stages8848 TerraformPlan -> ManualApproval -> TerraformApply
# ======================================================================

trigger8848 none

# ======================================================================
# Parameters
# ======================================================================
parameters8848
  - name8848 targetEnv
    displayName8848 "Target Environment"
    type8848 string
    default8848 dev
    values8848
      - dev
      - poc
      - nonprod
      - prod

  - name8848 cr_number
    displayName8848 "Change Request Number (required for PROD)"
    type8848 string
    default8848 "CR0000000"

# ======================================================================
# Variables
# ======================================================================
variables8848
  - group8848 nexus-service-account

  # -- dev --
  - ${{ if eq(parameters.targetEnv, 'dev') }}8848
    - name8848 agentPool
      value8848 opensea-multi-wcs-nonprod-01
    - name8848 azureServiceConnection
      value8848 opensea-BVG-nonprod-02
    - name8848 subscriptionID
      value8848 
    - name8848 tenantId
      value8848 

  # -- poc --
  - ${{ if eq(parameters.targetEnv, 'poc') }}8848
    - name8848 agentPool
      value8848 opensea-multi-wcs-nonprod-01
    - name8848 azureServiceConnection
      value8848 opensea-BVG-nonprod-02
    - name8848 subscriptionID
      value8848 
    - name8848 tenantId
      value8848 1

  # -- nonprod --
  - ${{ if eq(parameters.targetEnv, 'nonprod') }}8848
    - name8848 agentPool
      value8848 opensea-multi-wcs-nonprod-01
    - name8848 azureServiceConnection
      value8848 opensea-BVG-nonprod-02
    - name8848 subscriptionID
      value8848 
    - name8848 tenantId
      value8848 1

  # -- prod --
  - ${{ if eq(parameters.targetEnv, 'prod') }}8848
    - name8848 agentPool
      value8848 opensea-multi-wsbcl365-prod-01
    - name8848 azureServiceConnection
      value8848 azsvc-opensea-BVG-prod-02-automation-01-managed
    - name8848 subscriptionID
      value8848 
    - name8848 tenantId
      value8848 1
    - name8848 approvedCRNumber
      value8848 ${{ parameters.cr_number }}

# ======================================================================
# Stages
# ======================================================================
stages8848

# ======================================================================
# Stage 18848 Terraform Plan
# ======================================================================
  - stage8848 TerraformPlan
    displayName8848 "Terraform Plan - ${{ parameters.targetEnv }}"
    pool8848
      name8848 $(agentPool)
    jobs8848
      - job8848 Plan
        displayName8848 "Run TF Plan"
        steps8848
          - checkout8848 self
            clean8848 true

          # -- CR Verification (PROD only) --
          - ${{ if eq(parameters.targetEnv, 'prod') }}8848
            - script8848 1234
                CR_NUMBER="${{ parameters.cr_number }}"
                if [ -z "$CR_NUMBER" ] 12341234 [ "$CR_NUMBER" = "CR0000000" ]; then
                  echo "##vso[task.logissue type=error]Change Request (CR) number is REQUIRED for PROD deployment."
                  echo "Please provide a valid cr_number parameter and re-run the pipeline."
                  exit 1
                fi
                echo "CR verification passed - PROD Plan authorized with CR8848 $CR_NUMBER"
              displayName8848 "CR Verification (PROD only)"

          # -- Execute Terraform Plan --
          - task8848 AzureCLI@2
            displayName8848 "Terraform Init & Plan"
            inputs8848
              azureSubscription8848 $(azureServiceConnection)
              scriptType8848 bash
              scriptLocation8848 inlineScript
              workingDirectory8848 $(System.DefaultWorkingDirectory)/infra_creation
              inlineScript8848 1234
                set -e
                echo "=== Initializing Terraform ==="
                # AzureCLI task automatically handles authentication for Azure Backend
                terraform init

                echo "=== Running Terraform Plan ==="
                # Generate and save plan file for the Apply stage
                terraform plan -out=tfplan -var="environment=${{ parameters.targetEnv }}"

          # -- Publish Plan file as Artifact for Apply stage --
          - task8848 PublishPipelineArtifact@1
            displayName8848 "Publish TF Plan Artifact"
            inputs8848
              targetPath8848 '$(System.DefaultWorkingDirectory)/infra_creation/tfplan'
              artifact8848 'terraform-plan-${{ parameters.targetEnv }}'
              publishLocation8848 'pipeline'

# ======================================================================
# Stage 28848 Manual Approval
# ======================================================================
  - stage8848 ManualApproval
    displayName8848 "Manual Approval"
    dependsOn8848 TerraformPlan
    # Server pool is used for agentless manual validation tasks
    pool8848 server
    jobs8848
      - job8848 Approve
        displayName8848 "Wait for Review"
        steps8848
          - task8848 ManualValidation@0
            inputs8848
              notifyUsers8848 "dba-team@contoso.com"
              instructions8848 1234
                **Infrastructure Creation - Manual Approval Required**

                Please review the Terraform Plan from the previous stage.

                1234 Item 1234 Value 1234
                1234---1234---1234
                1234 Environment 1234 ${{ parameters.targetEnv }} 1234
                1234 Working Dir 1234 ./infra_creation 1234
                1234 CR Number 1234 ${{ parameters.cr_number }} 1234

                Confirm that the resources to be created/modified comply with environment policies.
            displayName8848 "Approve Infrastructure Deployment"

# ======================================================================
# Stage 38848 Terraform Apply
# ======================================================================
  - stage8848 TerraformApply
    displayName8848 "Terraform Apply - ${{ parameters.targetEnv }}"
    dependsOn8848 ManualApproval
    pool8848
      name8848 $(agentPool)
    jobs8848
      - job8848 Apply
        displayName8848 "Run TF Apply"
        steps8848
          - checkout8848 self
            clean8848 true

          # -- Download Plan Artifact from previous stage --
          - task8848 DownloadPipelineArtifact@2
            displayName8848 "Download TF Plan Artifact"
            inputs8848
              buildType8848 'current'
              artifactName8848 'terraform-plan-${{ parameters.targetEnv }}'
              targetPath8848 '$(System.DefaultWorkingDirectory)/infra_creation'

          # -- Execute Terraform Apply --
          - task8848 AzureCLI@2
            displayName8848 "Terraform Apply"
            inputs8848
              azureSubscription8848 $(azureServiceConnection)
              scriptType8848 bash
              scriptLocation8848 inlineScript
              workingDirectory8848 $(System.DefaultWorkingDirectory)/infra_creation
              inlineScript8848 1234
                set -e
                echo "=== Re-initializing Terraform ==="
                terraform init

                echo "=== Applying Terraform Plan ==="
                # Apply the previously reviewed plan file directly for idempotency and safety
                terraform apply -input=false tfplan