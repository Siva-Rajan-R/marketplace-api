from ..import ORGANAIZATION_YEAR,ORGANAIZATION_NAME,Optional,List,EmailStr

def get_user_registration_accept_email_content(
    name:str, email:EmailStr, description:str, shop_type:str, mobile_number:str,accept_url:str, delete_url:str,
    year:Optional[int]=ORGANAIZATION_YEAR, org_name:Optional[str]=ORGANAIZATION_NAME
):
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Registration Accept Request</title>
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
                margin-bottom:16px;">
                Registration Request
              </div>

              <h1 style="font-size:26px; color:#0f172a; margin:0 0 16px;">
                From {org_name}, {name}!
              </h1>

              <p style="font-size:14px; color:#475569; line-height:1.6;">
                Has initiated a registeration request
                Here are the details:
              </p>

              <!-- Details Box -->
              <div style="
                background:#f8fafc;
                border:1px solid #e2e8f0;
                padding:18px 20px;
                border-radius:10px;
                margin-top:20px;
                font-size:14px;
                color:#334155;
                line-height:1.6;
              ">
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Name:</strong> {name}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Email:</strong> {email}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Description:</strong> {description}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Shop Type:</strong> {shop_type}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Mobile Number:</strong> {mobile_number}</p>
              </div>

              <!-- Buttons Row -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;">
                <tr>

                  <!-- Accept Button -->
                  <td align="center" style="width:50%; padding-right:6px;">
                    <a href="{accept_url}"
                      style="
                        display:block;
                        width:100%;
                        text-align:center;
                        padding:14px 0;
                        font-size:15px;
                        font-weight:600;
                        color:#ffffff;
                        text-decoration:none;
                        background:linear-gradient(to right, #3b82f6, #2563eb);
                        border-radius:10px;
                        box-shadow:0 4px 12px rgba(37,99,235,0.35);
                      "
                    >
                      Accept
                    </a>
                  </td>

                  <!-- Delete Button -->
                  <td align="center" style="width:50%; padding-left:6px;">
                    <a href="{delete_url}"
                      style="
                        display:block;
                        width:100%;
                        text-align:center;
                        padding:14px 0;
                        font-size:15px;
                        font-weight:600;
                        color:#ffffff;
                        text-decoration:none;
                        background:#ef4444;
                        border-radius:10px;
                        box-shadow:0 4px 12px rgba(239,68,68,0.35);
                      "
                    >
                      Delete
                    </a>
                  </td>

                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 32px; font-size:11px; color:#94a3b8; background:#ffffff;">
              Thank you for registering with {org_name}. We're excited to have you!
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


def get_registration_received_email_content(name:str, email:EmailStr, description:str, shop_type:str, mobile_number:str, year:Optional[int]=ORGANAIZATION_YEAR, org_name:Optional[str]=ORGANAIZATION_NAME):
   return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Registration Successfull</title>
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
                margin-bottom:16px;">
                Registration Successfull
              </div>

              <h1 style="font-size:26px; color:#0f172a; margin:0 0 16px;">
                Welcome to {org_name}, {name}!
              </h1>

              <p style="font-size:14px; color:#475569; line-height:1.6;">
                Your registration has been successfully recived to our team. <b>We will be reach out you 2-3 bussiness days</b>
                Here are your details:
              </p>

              <!-- Details Box -->
              <div style="
                background:#f8fafc;
                border:1px solid #e2e8f0;
                padding:18px 20px;
                border-radius:10px;
                margin-top:20px;
                font-size:14px;
                color:#334155;
                line-height:1.6;
              ">
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Name:</strong> {name}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Email:</strong> {email}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Description:</strong> {description}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Shop Type:</strong> {shop_type}</p>
                <p style="margin:6px 0;"><strong style="color:#1e293b;">Mobile Number:</strong> {mobile_number}</p>
              </div>

              <!-- Buttons Row -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;">
                <tr>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 32px; font-size:11px; color:#94a3b8; background:#ffffff;">
              Thank you for registering with {org_name}. We're excited to have you!
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


def get_registeration_verified_email_content(name:str, email:EmailStr, login_url:str, org_name:Optional[str]=ORGANAIZATION_NAME, year:Optional[int]=ORGANAIZATION_YEAR):
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Shop Verification Successful</title>
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
                       background:linear-gradient(to right, #60a5fa, #3b82f6, #2563eb);">
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
                color:#1d4ed8;
                background:#dbeafe;
                border-radius:9999px;
                margin-bottom:16px;">
                Verification Successful
              </div>

              <h1 style="font-size:24px; color:#0f172a; margin:0 0 12px;">
                Hi {name},
              </h1>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:18px;">
                Great news! Your account
                has been successfully verified by our team.
              </p>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:18px;">
                You can now access your shop dashboard using your registered email:
              </p>

              <div style="
                background:#f8fafc;
                border:1px solid #e2e8f0;
                border-radius:10px;
                padding:14px 18px;
                font-size:14px;
                color:#334155;
                margin-bottom:24px;
              ">
                <strong style="color:#1e293b;">Login Email:</strong> {email}
              </div>

              <!-- Button -->
              <a href="{login_url}"
                style="
                  display:block;
                  width:100%;
                  text-align:center;
                  padding:14px 0;
                  font-size:15px;
                  font-weight:600;
                  color:#ffffff;
                  background:linear-gradient(to right, #3b82f6, #2563eb);
                  border-radius:10px;
                  text-decoration:none;
                  box-shadow:0 4px 12px rgba(37,99,235,0.35);
                ">
                Access Your Shop
              </a>

              <p style="font-size:14px; color:#475569; margin-top:22px;">
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


def get_registeration_failed_email_content(name:str, description:str, org_name:Optional[str]=ORGANAIZATION_NAME, year:Optional[int]=ORGANAIZATION_YEAR):
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Verification Unsuccessful</title>
</head>

<body style="margin:0; padding:0; background:#f1f5f9; font-family:Arial, Helvetica, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9; padding:40px 0;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0"
               style="max-width:520px; background:#ffffff; border-radius:14px;
               overflow:hidden; border:1px solid #e2e8f0;">

          <!-- Red Header -->
          <tr>
            <td style="height:6px; background:linear-gradient(to right, #f87171, #ef4444, #dc2626);"></td>
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
                color:#b91c1c;
                background:#fee2e2;
                border-radius:9999px;
                margin-bottom:16px;">
                Verification Unsuccessful
              </div>

              <h1 style="font-size:24px; color:#0f172a; margin:0 0 12px;">
                Hi {name},
              </h1>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:18px;">
                Unfortunately, we were unable to verify your account
              </p>

              <p style="font-size:15px; color:#475569; line-height:1.7; margin-bottom:18px;">
                The verification process could not be completed due to missing or insufficient details.
                Here’s the reason provided:
              </p>

              <!-- Description Box -->
              <div style="
                background:#fef2f2;
                border:1px solid #fca5a5;
                border-radius:10px;
                padding:14px 18px;
                font-size:14px;
                color:#b91c1c;
                margin-bottom:24px;
                line-height:1.6;
              ">
                {description}
              </div>

              <p style="font-size:14px; color:#475569; line-height:1.7;">
                You may update your details and register again anytime.
                If you believe this decision was a mistake, feel free to contact our support team.
              </p>

              <p style="font-size:14px; color:#475569; margin-top:24px;">
                Regards,<br>
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

