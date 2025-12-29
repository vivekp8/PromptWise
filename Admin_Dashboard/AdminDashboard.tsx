import PromptReviewQueue from './PromptReviewQueue'
import MetricsPanel from './MetricsPanel'
import ExportHistoryPanel from './ExportHistoryPanel'
import RoleManager from './RoleManager'
import AuditLogTable from './AuditLogTable'
import AlertBell from './AlertBell'
import FlaggedContentList from './FlaggedContentList'
import PasswordSettings from './PasswordSettings'

export default function AdminDashboard() {
  return (
    <div className="admin-dashboard">
      <AlertBell />
      <PromptReviewQueue />
      <FlaggedContentList />
      <MetricsPanel />
      <ExportHistoryPanel />
      <RoleManager />
      <AuditLogTable />
      <PasswordSettings userId="vivek_admin" />
    </div>
  )
}
