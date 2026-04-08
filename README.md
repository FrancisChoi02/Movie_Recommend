# ============================================================
# Unified CICD Pipeline – pp-openai-monitor-dashboard
# ============================================================
# Supports: CI only, CD only, or full CICD
# Environments: dev, poc, nonprod, prod
#
# PROD deployments require a Change Request (CR) number.
# To add manual approval gates for PROD, configure an
# "Environment" with checks in Azure DevOps → Pipelines → Environments.
# ============================================================

trigger: none
pr: none

name: 'CICD-$(Build.BuildId)-${{ parameters.appVersion }}'

# ──────────────────────────────────────────────
# Parameters
# ──────────────────────────────────────────────
parameters:
  # ── Mode Selection ──
  - name: pipelineMode
    displayName: 'Pipeline Mode'
    type: string
    default: CICD
    values:
      - CI
      - CD
      - CICD

  # ── Target Environment ──
  - name: targetEnv
    displayName: 'Target Environment'
    type: string
    default: nonprod
    values:
      - dev
      - poc
      - nonprod
      - prod

  # ── CI Parameters ──
  - name: appName
    displayName: 'Application Name'
    type: string
    default: pp-openai-monitor-dashboard

  - name: appVersion
    displayName: 'Application Version'
    type: string
    default: 0.1.8_1

  - name: groupId
    displayName: 'Maven Group ID'
    type: string
    default: com.BAG.wsit.rgl.powerplatform.artifacts.genai

  - name: github_branch
    displayName: 'Git Branch (CI stage only)'
    type: string
    default: gpt_4_1_test

  # ── CD Parameters ──
  - name: pkg_DIPDIVE_url
    displayName: 'DIPDIVE Package URL (required for CD-only mode; leave empty for CICD)'
    type: string
    default: ''

  - name: co_number
    displayName: 'Change Request Number (required for PROD deployment)'
    type: string
    default: ''

# ──────────────────────────────────────────────
# Variables
# ──────────────────────────────────────────────
variables:
  # Common
  - group: DIPDIVE-service-account
  - name: packageName
    value: '${{ parameters.appName }}-${{ parameters.appVersion }}.zip'
  - name: DIPDIVE_url
    value: https://DIPDIVE304.systems.uk.BAG:8081/DIPDIVE/repository/maven-BAG-internal-dev_n3p

  # ── Environment-specific mappings ──
  # dev (update webappName / webappResourceGroup to actual values)
  - ${{ if eq(parameters.targetEnv, 'dev') }}:
    - name: agentPool
      value: BAG-multi-wcs-nonprod-01
    - name: azureServiceConnection
      value: OPENSEA-nonprod-01
    - name: webappName
      value: OPENSEA-nonprod-use-monitor-dashboard-dev
    - name: webappResourceGroup
      value: OPENSEA-nonprod-use-monitor-dashboard-dev

  # poc (update webappName / webappResourceGroup to actual values)
  - ${{ if eq(parameters.targetEnv, 'poc') }}:
    - name: agentPool
      value: BAG-multi-wcs-nonprod-01
    - name: azureServiceConnection
      value: OPENSEA-nonprod-01
    - name: webappName
      value: OPENSEA-nonprod-use-monitor-dashboard-poc
    - name: webappResourceGroup
      value: OPENSEA-nonprod-use-monitor-dashboard-poc

  # nonprod / UAT
  - ${{ if eq(parameters.targetEnv, 'nonprod') }}:
    - name: agentPool
      value: BAG-multi-wcs-nonprod-01
    - name: azureServiceConnection
      value: OPENSEA-nonprod-01
    - name: webappName
      value: OPENSEA-nonprod-use-monitor-dashboard-uat
    - name: webappResourceGroup
      value: OPENSEA-nonprod-use-monitor-dashboard-uat

  # prod
  - ${{ if eq(parameters.targetEnv, 'prod') }}:
    - name: agentPool
      value: OPENSEA-prod-01
    - name: azureServiceConnection
      value: azsvc-OPENSEA-prod-01-automation-01-managed
    - name: webappName
      value: OPENSEA-prod-use-monitor-dashboard-prod
    - name: webappResourceGroup
      value: OPENSEA-prod-use-monitor-dashboard-prod
    - name: approvedCRNumber
      value: ${{ parameters.co_number }}

# ──────────────────────────────────────────────
# Stages
# ──────────────────────────────────────────────
stages:

  # ──────────────────────────────────────────
  # CI – Build & Publish to DIPDIVE
  # ──────────────────────────────────────────
  - ${{ if or(eq(parameters.pipelineMode, 'CI'), eq(parameters.pipelineMode, 'CICD')) }}:
    - stage: CI
      displayName: 'CI – Build & Publish'
      jobs:
        - job: BuildAndPublish
          displayName: 'Build & Publish to DIPDIVE'
          pool:
            name: BAG-multi-wcs-nonprod-01   # CI always builds on nonprod pool
          steps:
            - checkout: self
              persistCredentials: true

            - script: |
                set -euo pipefail
                echo "=== CI: Building ${{ parameters.appName }} v${{ parameters.appVersion }} ==="
                echo "Clone with branch ${{ parameters.github_branch }}"
                git clone --single-branch \
                  --branch "${{ parameters.github_branch }}" \
                  "https://$(DIPDIVEusername):$(DIPDIVEpassword)@alm-github.systems.uk.BAG/cmb-regional-asp/pp-openai-monitor-dashboard.git"
                ls
                cd "pp-openai-monitor-dashboard"
                python --version
                python -m venv antenv
                source antenv/bin/activate
                export PIP_NO_INPUT=1
                export PIP_DISABLE_PIP_VERSION_CHECK=1
                pip install --upgrade pip setuptools
                pip install -r requirements.txt
              displayName: 'Set up Python environment and install requirements'
              workingDirectory: $(System.DefaultWorkingDirectory)
              env:
                PIP_INDEX_URL: 'https://$(DIPDIVEusername):$(DIPDIVEpassword)@DIPDIVE302.systems.uk.BAG:8081/DIPDIVE/repository/pypi-group/simple'
                PIP_NO_INPUT: '1'
                PIP_DISABLE_PIP_VERSION_CHECK: '1'

            - task: ArchiveFiles@2
              displayName: 'Archive files'
              inputs:
                rootFolderOrFile: '$(System.DefaultWorkingDirectory)/pp-openai-monitor-dashboard'
                includeRootFolder: false
                archiveType: zip
                archiveFile: $(packageName)
                replaceExistingArchive: true

            - script: |
                echo "Pushing - artifactId=${{ parameters.appName }}, version=${{ parameters.appVersion }}, packageName=$(packageName)..."
                curl -s -f --show-error --user $(DIPDIVEusername):$(DIPDIVEpassword) \
                  -X POST 'https://DIPDIVE304.systems.uk.BAG:8081/DIPDIVE/service/rest/v1/components?repository=maven-BAG-internal-dev_n3p' \
                  -F maven2.groupId=${{ parameters.groupId }} \
                  -F maven2.artifactId=${{ parameters.appName }} \
                  -F maven2.version=${{ parameters.appVersion }} \
                  -F maven2.asset1=@$(packageName) \
                  -F maven2.asset1.extension=zip
              displayName: 'Push application package to DIPDIVE'
              workingDirectory: $(System.DefaultWorkingDirectory)

  # ──────────────────────────────────────────
  # CD – Download & Deploy to target environment
  # ──────────────────────────────────────────
  - ${{ if or(eq(parameters.pipelineMode, 'CD'), eq(parameters.pipelineMode, 'CICD')) }}:
    - stage: CD
      displayName: 'CD – Deploy to ${{ parameters.targetEnv }}'
      ${{ if eq(parameters.pipelineMode, 'CICD') }}:
        dependsOn: CI
      jobs:
        - job: Deploy
          displayName: 'Deploy to ${{ parameters.targetEnv }}'
          pool:
            name: $(agentPool)
          steps:
            - checkout: self
              persistCredentials: true

            # ── Validate required parameters ──
            - script: |
                if [ "${{ parameters.pipelineMode }}" = "CD" ] && [ -z "${{ parameters.pkg_DIPDIVE_url }}" ]; then
                  echo "##vso[task.logissue type=error]pkg_DIPDIVE_url is required when running in CD-only mode."
                  exit 1
                fi
              displayName: 'Validate Parameters'

            # ── CR Verification (PROD only) ──
            - ${{ if eq(parameters.targetEnv, 'prod') }}:
              - script: |
                  if [ -z "${{ parameters.co_number }}" ]; then
                    echo "##vso[task.logissue type=error]Change Request (CR) number is REQUIRED for PROD deployment."
                    echo "Please provide the co_number parameter and re-run the pipeline."
                    exit 1
                  fi
                  echo "##vso[task.setvariable variable=approvedCRNumber]${{ parameters.co_number }}"
                  echo "CR verification passed. Deploying to PROD with CR: ${{ parameters.co_number }}"
                displayName: 'CR Verification'

            # ── Download Package from DIPDIVE ──
            - script: |
                # Resolve package URL based on pipeline mode
                if [ "${{ parameters.pipelineMode }}" = "CICD" ]; then
                  # In CICD mode, construct URL from the package just published by CI
                  DIPDIVEBaseUrl="$(DIPDIVE_url)"
                  groupIdPath="${{ parameters.groupId }}"
                  groupIdPath="${groupIdPath//.//}"
                  pkgUrl="${DIPDIVEBaseUrl}/${groupIdPath}/${{ parameters.appName }}/${{ parameters.appVersion }}/${{ parameters.appName }}-${{ parameters.appVersion }}.zip"
                else
                  # In CD-only mode, use the user-provided URL
                  pkgUrl="${{ parameters.pkg_DIPDIVE_url }}"
                fi

                echo "Download package from ${pkgUrl}"
                curl -v --user $(DIPDIVEusername):$(DIPDIVEpassword) "${pkgUrl}" -o ${{ parameters.appName }}.zip

                ls -l
                maxsize=2000
                filesize=$(stat -c%s "${{ parameters.appName }}.zip")
                echo "Size of ${{ parameters.appName }}.zip = $filesize bytes."
                if (( filesize < maxsize )); then
                  echo "##vso[task.logissue type=error]Error downloading file. File too small or download failed. Exiting."
                  exit 1
                fi
              displayName: 'Download Package from DIPDIVE'

            # ── Deploy to Azure App Service ──
            - task: AzureCLI@2
              name: deploy_webapp_to_azure
              displayName: 'Azure App Service Deploy: $(webappName)'
              enabled: true
              inputs:
                azureSubscription: $(azureServiceConnection)
                scriptType: bash
                scriptLocation: inlineScript
                addSpnToEnvironment: true
                inlineScript: |
                  ls -la
                  az webapp deployment source config-zip \
                    --resource-group $(webappResourceGroup) \
                    --name $(webappName) \
                    --src ./${{ parameters.appName }}.zip
