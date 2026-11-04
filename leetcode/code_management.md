```mermaid
**Artifact Versioning and Release Management Policy**

**I. Core Principles**

1. **Unified Release Planning:** All target version numbers (following Semantic Versioning: MAJOR.MINOR.PATCH) shall be centrally planned and allocated via the *Release Registry Matrix*. Unauthorized assignment or modification of major/minor version numbers by individual developers is strictly prohibited.
2. **Artifact Immutability:** Every generated artifact must possess a globally unique version identifier. Overwriting, replacing, or forcibly pushing to an existing artifact tag in the artifact repository is strictly forbidden.
3. **Artifact Promotion Model:** The final production artifact shall **never be recompiled**. Production releases must be executed by directly promoting (re-tagging) the exact Release Candidate (RC) artifact that successfully passed QA validation.

**II. Release Stages & Naming Conventions**

| Release Phase | Associated Branch | Artifact Version Format | Example | Description |
| --- | --- | --- | --- | --- |
| **1. Feature Development (Dev)** | `feat-xxx` | `<TARGET_VERSION>-<BRANCH_NAME>.<SHORT_HASH>` | `0.2.0-feat-login.a1b2c3d` | Utilized for local and isolated environment testing. The Git commit hash guarantees strict version uniqueness. |
| **2. Release Candidate (RC)** | `release-<TARGET_VERSION>` | `<TARGET_VERSION>-rc.<BUILD_NUMBER>` | `0.2.0-rc.1` | Triggered post-code freeze. Feature branches are merged into the release branch to generate an RC artifact for comprehensive QA regression testing. |
| **3. Production Release (Prod)** | `main` (with Tag) | `<TARGET_VERSION>` | `0.2.0` | Upon RC approval, the CI/CD pipeline seamlessly promotes the verified `rc.X` artifact to the formal production release. Code is subsequently merged into the main trunk. |

**III. Standard Operating Procedures (SOP)**

1. **Pre-Release (Scheduling & Allocation):** Technical Leads or Product Managers must register the upcoming release cycle (e.g., `0.2.0`) in the *Release Registry Matrix* prior to development. All concurrent feature branches shall base their CI configurations on this target version.
2. **Active Release (Integration & Code Freeze):** Upon reaching the established QA cut-off date, all completed feature branches must be merged into the designated `release-X.X.X` branch. A strict code freeze is enacted immediately; thereafter, only targeted bug fixes for the current release are permitted to be merged.
3. **Post-Release (Archiving & Transition):** Following a successful production deployment, the version status in the registry must be updated to "Released." The release branch is merged into `main`, and development for the subsequent iteration shall commence by branching off the updated `main` branch.
```

```mermaid
graph TD
    subgraph 1_Dev ["1. Development Stage"]
        F_A[Branch: feat-A] -->|CI Build| Art_A(Artifact: 0.2.0-feat-A.a1b2)
        F_B[Branch: feat-B] -->|CI Build| Art_B(Artifact: 0.2.0-feat-B.c3d4)
    end

    subgraph 2_QA ["2. Integration & QA Stage"]
        F_A -.Code Freeze<br/>Merge Code.-> Rel_Branch[Branch: release-0.2.0]
        F_B -.Code Freeze<br/>Merge Code.-> Rel_Branch
        Rel_Branch -->|CI Unified Build| Art_RC(Artifact: 0.2.0-rc.1)
        Art_RC --> QA{QA Regression Testing}
        
        QA -- Bug Found --> Fix[Fix in release branch]
        Fix -->|CI Rebuild| Art_RC2(Artifact: 0.2.0-rc.2)
        Art_RC2 --> QA
    end

    subgraph 3_Prod ["3. Artifact Promotion & Production"]
        QA -- Test Passed --> Promote[Execute Promotion<br/>⚠️ STRICTLY NO RECOMPILATION]
        
        Promote ===>|Directly Retag Artifact| Art_Prod((Final Artifact: 0.2.0))
        Promote -.Code Archiving.-> Main[Branch: main]
    end

    classDef artifact fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef highlight fill:#fff3cd,stroke:#ffeeba,stroke-width:2px,color:#856404;
    class Art_A,Art_B,Art_RC,Art_RC2 artifact;
    class Art_Prod highlight;
```