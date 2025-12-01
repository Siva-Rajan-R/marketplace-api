def get_employee_accept_email_content(shop_name:str, role:str, accept_url:str, year:int,company_name:str):
    return f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Shop Invitation</title>
  </head>

  <body style="margin:0; padding:0; background:#f1f5f9; font-family:Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9; padding:40px 0;">
      <tr>
        <td align="center">

          <!-- Card -->
          <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px; background:#ffffff; border-radius:14px; overflow:hidden; border:1px solid #e2e8f0;">
            
            <!-- Gradient Header -->
            <tr>
              <td style="height:6px; background:linear-gradient(to right, #60a5fa, #3b82f6, #2563eb);"></td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:32px;">

                <!-- Badge -->
                <div style="
                  display:inline-block;
                  padding:6px 12px;
                  font-size:12px;
                  font-weight:600;
                  color:#1d4ed8;
                  background:#dbeafe;
                  border-radius:9999px;
                  margin-bottom:16px;"
                >
                  Invitation to collaborate
                </div>

                <h1 style="font-size:26px; color:#0f172a; margin:0 0 12px;">
                  You’re invited to join <span style="color:#2563eb;">{shop_name}</span>
                </h1>

                <p style="font-size:15px; color:#475569; line-height:1.6;">
                  You have been invited to work on
                  <strong style="color:#0f172a;">{shop_name}</strong>
                  as a
                  <strong style="color:#2563eb;">{role}</strong>.
                </p>

                <p style="font-size:14px; color:#475569; line-height:1.6; margin-top:16px;">
                  If you're willing to accept this invite, click the button below.
                  If not, you may ignore this email.
                </p>

                <p style="font-size:12px; color:#64748b; margin-top:14px;">
                  This invitation link automatically expires in
                  <strong style="color:#0f172a;">5 minutes</strong>.
                </p>

                <!-- Button -->
                <div style="text-align:center; margin:28px 0;">
                  <a href="{accept_url}"
                    style="
                      display:inline-block;
                      padding:12px 24px;
                      font-size:15px;
                      font-weight:600;
                      color:#ffffff;
                      background:linear-gradient(to right, #3b82f6, #2563eb);
                      border-radius:10px;
                      text-decoration:none;
                      box-shadow:0 4px 10px rgba(59,130,246,0.3);
                    "
                  >
                    Accept Invite
                  </a>
                </div>

                <p style="font-size:11px; color:#64748b; line-height:1.6;">
                  If the button doesn't work, copy this link into your browser:<br>
                  <span style="color:#2563eb; word-break:break-all;">{accept_url}</span>
                </p>

              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="padding:16px 32px; font-size:11px; color:#94a3b8; background:#ffffff;">
                If you did not expect this invitation, you may safely ignore this email.
              </td>
            </tr>

          </table>

          <div style="font-size:11px; color:#94a3b8; margin-top:10px;">
            &copy; {year} {company_name}. All rights reserved.
          </div>

        </td>
      </tr>
    </table>
  </body>
</html>
"""
