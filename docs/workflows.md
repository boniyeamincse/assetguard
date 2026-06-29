# Workflows, Roles & Policies

This document outlines the operational procedures, access controls, and scoring algorithms built into AssetGuard.

## User Roles & Permissions

AssetGuard features a strict role-based access control (RBAC) system with 5 defined roles:

| Feature | Super Admin | Security | Software | Owner | Management |
|---------|-------------|----------|----------|-------|-----------|
| Dashboard | Full | Related | Assigned | Own | Read-only |
| Users | Full | No | No | No | No |
| Teams | Full | View | View | No | No |
| Assets | Full | View/Create | View | Own | View |
| Vulnerabilities | Full | Create/Edit/Retest | Assign Update | View/Comment | View |
| Reports | Full | Security Reports | Assigned | Own Reports | View |
| Audit Logs | Full | No | No | No | No |

## Vulnerability Workflow

### Normal Workflow
```
New → Triaged → Assigned → In Progress → Fixed 
→ Ready for Retest → Retesting → Verified Fixed → Closed
```

### Failed Retest Workflow
```
Ready for Retest → Retesting → Reopened → Assigned 
→ In Progress → Fixed → Ready for Retest
```

### Alternative Workflows
- **Risk Accepted**: Directly from New/Triaged/Assigned
- **Rejected**: From New/Triaged

## SLA Policy

Recommended response times for handling vulnerabilities based on severity:
- **Critical**: 24-48 hours
- **High**: 3-7 days
- **Medium**: 15 days
- **Low**: 30 days
- **Informational**: Best effort

## Risk Score Calculation

The asset risk score is calculated dynamically based on the severity of its open vulnerabilities.

Formula:
```
(Critical Open × 10) + (High Open × 7) + (Medium Open × 4) + (Low Open × 2) + (Informational Open × 1)
```

Risk ratings threshold:
- **0-10**: Low Risk
- **11-30**: Medium Risk
- **31-60**: High Risk
- **61+**: Critical Risk
