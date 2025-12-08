from ..import ORGANAIZATION_YEAR,ORGANAIZATION_NAME,Optional,List

def get_employee_accept_req_email_content(shop_name:str, role:str, accept_url:str,employee_name:str, year:Optional[int]=ORGANAIZATION_YEAR,company_name:Optional[str]=ORGANAIZATION_NAME):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{company_name} – Employee Invitation</title>
</head>

<body style="margin:0; padding:0; background:#f3f4f6; font-family:Arial, sans-serif;">

<!-- MAIN WRAPPER -->
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f6; padding:20px 0;">
  <tr>
    <td align="center">

      <!-- CARD -->
      <table width="100%" cellpadding="0" cellspacing="0" 
             style="max-width:640px; background:#ffffff; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">

        <!-- HEADER -->
        <tr>
          <td style="background:#4f46e5; padding:20px; text-align:center;">
            <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:bold;">
              {company_name}
            </h1>
          </td>
        </tr>

        <!-- BODY -->
        <tr>
          <td style="padding:24px;">

            <h2 style="margin:0; text-align:center; font-size:20px; color:#111827; font-weight:bold;">
              Employee Invitation
            </h2>

            <p style="margin:16px 0; text-align:center; color:#374151; font-size:15px; line-height:1.6;">
              Hello <strong>{employee_name}</strong>,<br>
              You have been invited to join <strong>{shop_name}</strong>.
            </p>

            <!-- INFO CARD -->
            <table width="100%" cellpadding="0" cellspacing="0" 
                   style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:8px; padding:16px;">

              <!-- Shop Row -->
              <tr>
                <td style="padding-bottom:10px;">
                  <p style="margin:0; font-size:11px; color:#6b7280; text-transform:uppercase; font-weight:bold;">
                    Shop Name
                  </p>
                  <p style="margin:4px 0 0; color:#111827; font-size:14px;">
                    {shop_name}
                  </p>
                </td>
              </tr>

              <!-- Role Row -->
              <tr>
                <td style="padding-bottom:10px;">
                  <p style="margin:0; font-size:11px; color:#6b7280; text-transform:uppercase; font-weight:bold;">
                    Assigned Role
                  </p>
                  <p style="margin:4px 0 0; color:#111827; font-size:14px;">
                    {role}
                  </p>
                </td>
              </tr>

              <!-- Expiry Row -->
              <tr>
                <td>
                  <p style="margin:0; font-size:11px; color:#6b7280; text-transform:uppercase; font-weight:bold;">
                    Invitation Validity
                  </p>
                  <p style="margin:4px 0 0; color:#111827; font-size:14px;">
                    This invitation will automatically expire in <strong>5 minutes</strong>.
                  </p>
                </td>
              </tr>

            </table>

            <!-- FULL-WIDTH ACCEPT BUTTON -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:24px;">
              <tr>
                <td>
                  <a href="{accept_url}" 
                    style="
                      display:block;
                      width:100%;
                      text-align:center;
                      background:#16a34a;
                      color:#ffffff;
                      padding:14px 0;
                      text-decoration:none;
                      border-radius:6px;
                      font-size:16px;
                      font-weight:bold;
                    ">
                    Accept Invitation
                  </a>
                </td>
              </tr>
            </table>

            <!-- WARNING BOX -->
            <table width="100%" cellpadding="0" cellspacing="0" 
                   style="margin-top:24px; background:#fef9c3; border-left:4px solid #facc15; padding:12px; border-radius:6px;">
              <tr>
                <td>
                  <p style="margin:0; color:#854d0e; font-size:14px; font-weight:bold;">
                    ⚠ Security Notice
                  </p>
                  <p style="margin:6px 0 0; color:#854d0e; font-size:14px; line-height:1.5;">
                    If you did not expect this invitation or see suspicious activity,
                    report it immediately to:
                    <br><strong>report@marketplace.com</strong>
                  </p>
                </td>
              </tr>
            </table>

            <!-- FOOTER -->
            <p style="text-align:center; margin-top:32px; color:#6b7280; font-size:12px; line-height:1.6;">
              This is an automated email from © {year} {company_name}.<br>
              If you didn’t request this, please ignore it.
            </p>

          </td>
        </tr>

      </table>
      <!-- End Card -->

    </td>
  </tr>
</table>
</body>
</html>

"""


def get_employee_accepted_email_content(
    name: str,
    email: str,
    shop_name: str,
    role: str,
    dashboard_url: str,
    org_name: str = ORGANAIZATION_NAME,
    year: int = ORGANAIZATION_YEAR
):
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Invitation Accepted</title>
</head>

<body style="margin:0; padding:0; background:#f1f5f9; font-family:Arial, Helvetica, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9; padding:40px 0;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0"
               style="max-width:520px; background:#ffffff; border-radius:14px;
               overflow:hidden; border:1px solid #e2e8f0;">

          <!-- Gradient Top -->
          <tr>
            <td style="height:6px;
                       background:linear-gradient(to right, #22c55e, #16a34a, #15803d);">
            </td>
          </tr>

          <!-- Content -->
          <tr>
            <td style="padding:32px;">

              <!-- Badge -->
              <div style="
                display:inline-block;
                padding:6px 12px;
                font-size:12px;
                font-weight:600;
                color:#166534;
                background:#dcfce7;
                border-radius:9999px;
                margin-bottom:16px;">
                Invitation Accepted
              </div>

              <h1 style="font-size:24px; color:#0f172a; margin:0 0 12px;">
                Hi {name},
              </h1>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:18px;">
                You have successfully accepted the invitation to join
                <strong style="color:#0f172a;">{shop_name}</strong>.
              </p>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:20px;">
                Below are your account details:
              </p>

              <!-- INFO BOX -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f8fafc; border:1px solid #e2e8f0;
                     border-radius:12px; padding:16px; margin-bottom:24px;">

                <!-- Email -->
                <tr>
                  <td style="padding-bottom:10px;">
                    <p style="margin:0; font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">
                      Login Email
                    </p>
                    <p style="margin:4px 0 0; color:#0f172a; font-size:14px;">
                      {email}
                    </p>
                  </td>
                </tr>

                <!-- Shop -->
                <tr>
                  <td style="padding-bottom:10px;">
                    <p style="margin:0; font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">
                      Shop Name
                    </p>
                    <p style="margin:4px 0 0; color:#0f172a; font-size:14px;">
                      {shop_name}
                    </p>
                  </td>
                </tr>

                <!-- Role -->
                <tr>
                  <td>
                    <p style="margin:0; font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">
                      Assigned Role
                    </p>
                    <p style="margin:4px 0 0; color:#0f172a; font-size:14px;">
                      {role}
                    </p>
                  </td>
                </tr>

              </table>

              <!-- Button -->
              <a href="{dashboard_url}"
                style="
                  display:block;
                  width:100%;
                  text-align:center;
                  padding:14px 0;
                  font-size:15px;
                  font-weight:600;
                  color:#ffffff;
                  background:linear-gradient(to right, #16a34a, #15803d);
                  border-radius:10px;
                  text-decoration:none;
                  box-shadow:0 4px 10px rgba(22,163,74,0.35);
                ">
                Go to Dashboard
              </a>

              <!-- Security Warning -->
              <div style="
                margin-top:24px;
                padding:16px;
                background:#fef9c3;
                border-left:4px solid #facc15;
                border-radius:8px;
                font-size:14px;
                line-height:1.6;
                color:#854d0e;
              ">
                <strong>⚠ Security Notice:</strong><br>
                If this action wasn't performed by you or seems suspicious,
                please contact our support team immediately.
              </div>

              <p style="font-size:14px; color:#475569; margin-top:24px;">
                Welcome aboard,<br>
                <strong style="color:#0f172a;">{org_name} Team</strong>
              </p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 32px; font-size:11px; color:#94a3b8; background:#ffffff;">
              This is an automated message. Please do not reply to this email.
            </td>
          </tr>

        </table>

        <div style="font-size:11px; color:#94a3b8; margin-top:10px;">
          &copy; {year} {org_name}. All rights reserved.
        </div>

      </td>
    </tr>
  </table>

</body>
</html>
"""

