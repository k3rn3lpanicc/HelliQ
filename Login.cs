using System;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using System.Threading;
using System.IO;
using Helli_Registeration_Form;
using MySql.Data.MySqlClient;
using System.Data;
using System.Net;
using System.Collections.Specialized;
using Newtonsoft.Json.Linq;
using System.Globalization;
using Helli_Registeration_Form;

namespace EasyLogin
{

    public partial class Login : Form
    {
        class Web
        {
            public static string GetPost(string Url, params string[] postdata)
            {
                string result = string.Empty;
                string data = string.Empty;

                System.Text.ASCIIEncoding ascii = new ASCIIEncoding();

                if (postdata.Length % 2 != 0)
                {
                    MessageBox.Show("Parameters must be even , \"user\" , \"value\" , ... etc", Application.ProductName, MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return string.Empty;
                }

                for (int i = 0; i < postdata.Length; i += 2)
                {
                    data += string.Format("&{0}={1}", postdata[i], postdata[i + 1]);
                }

                data = data.Remove(0, 1);

                byte[] bytesarr = ascii.GetBytes(data);
                try
                {
                    WebRequest request = WebRequest.Create(Url);

                    request.Method = "POST";
                    request.ContentType = "application/x-www-form-urlencoded";
                    request.ContentLength = bytesarr.Length;

                    System.IO.Stream streamwriter = request.GetRequestStream();
                    streamwriter.Write(bytesarr, 0, bytesarr.Length);
                    streamwriter.Close();

                    WebResponse response = request.GetResponse();
                    streamwriter = response.GetResponseStream();

                    System.IO.StreamReader streamread = new System.IO.StreamReader(streamwriter);
                    result = streamread.ReadToEnd();
                    streamread.Close();
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message, Application.ProductName, MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                return result;
            }
        }




        double sa = 0;

        //For keeping form on top
        private static readonly IntPtr HWND_TOPMOST = new IntPtr(-1);
        private const UInt32 SWP_NOSIZE = 0x0001;
        private const UInt32 SWP_NOMOVE = 0x0002;
        private const UInt32 TOPMOST_FLAGS = SWP_NOMOVE | SWP_NOSIZE;

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
        //---What then?


        [DllImport("user32.dll")]
        static extern int ReleaseCapture();
        [DllImport("user32.dll", EntryPoint = "SendMessageA")]
        static extern int SendMessage(int hwnd, int wMsg, int wParam, object lParam);
        private const int WM_NCLBUTTONDOWN = 161;

        [DllImport("user32.dll")]
        private static extern IntPtr SendMessage(HandleRef hWnd, uint Msg, int wParam, [MarshalAs(UnmanagedType.LPWStr)] String lParam);



        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        static extern bool BlockInput(bool fBlockIt);
        double zaman = 0.5;
        bool letcheck = true;
        public Login()
        {

            InitializeComponent();

            SendMessage(new HandleRef(txtUser, txtUser.Handle), 0x1501, 0, "نام کاربری");
            SendMessage(new HandleRef(Shenase_txt, Shenase_txt.Handle), 0x1501, 0, "شناسه دبیرستان");
            SendMessage(new HandleRef(txtPass, txtPass.Handle), 0x1501, 0, "کلمه عبور");
            //tempHeight = Srn.Bounds.Width;
            //tempWidth = Srn.Bounds.Height;
        }
        private const int CS_DROPSHADOW = 0x00020000;


        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            ReleaseCapture();
            SendMessage(this.Handle.ToInt32(), WM_NCLBUTTONDOWN, 2, 0);
        }
        protected override CreateParams CreateParams

        {

            get

            {

                CreateParams p = base.CreateParams;

                p.ClassStyle |= CS_DROPSHADOW;

                return p;

            }

        }


    string user = "";
        string pass = "";
          public static string Encrypt(string input, string key)
        {
            if (input == null)
            {
                input = " ";
            }
            byte[] inputArray = UTF8Encoding.UTF8.GetBytes(input);
            TripleDESCryptoServiceProvider tripleDES = new TripleDESCryptoServiceProvider();
            tripleDES.Key = UTF8Encoding.UTF8.GetBytes(key);
            tripleDES.Mode = CipherMode.ECB;
            tripleDES.Padding = PaddingMode.PKCS7;
            ICryptoTransform cTransform = tripleDES.CreateEncryptor();
            byte[] resultArray = cTransform.TransformFinalBlock(inputArray, 0, inputArray.Length);
            tripleDES.Clear();



            return Convert.ToBase64String(resultArray, 0, resultArray.Length);
        }
        public static string Decrypt(string input, string key)
        {
            if (input == null)
            {
                input = " ";
            }
            byte[] inputArray = Convert.FromBase64String(input);
            TripleDESCryptoServiceProvider tripleDES = new TripleDESCryptoServiceProvider();
            tripleDES.Key = UTF8Encoding.UTF8.GetBytes(key);
            tripleDES.Mode = CipherMode.ECB;
            tripleDES.Padding = PaddingMode.PKCS7;
            ICryptoTransform cTransform = tripleDES.CreateDecryptor();
            byte[] resultArray = cTransform.TransformFinalBlock(inputArray, 0, inputArray.Length);
            tripleDES.Clear();

            return UTF8Encoding.UTF8.GetString(resultArray);



        }



    string ss() {
            string machinname = Environment.MachineName;
            string username = Environment.UserName;
            string OS = Environment.OSVersion.ToString();
            string Code = Encrypt(machinname,"abcd-efgh-ijklmn")+Encrypt(username, "efgh-abcd-ijklmn") +Encrypt(OS, "ijklmn-efgh-abcd");
            string value = "";
            if (Code.Length%2!=1) {
                Code += "F";
            }
            for (int i=2;i<=Code.Length;i+=2) {
                value += Code[i];
            }


            return value;
        }
        bool busy = false;
           private void Login_Load(object sender, EventArgs e)
        {
            Shenase_txt.Focus();
            Opacity = 0;
            panel1.Location = new Point(Width / 2 - panel1.Width / 2, Height / 2 - panel1.Height / 2);
            System.Threading.Thread.Sleep(1);
            Application.DoEvents();
            Opacity = 0.96;
            //  MessageBox.Show(Opacity.ToString());    

            Application.DoEvents();
            this.MouseDown += new MouseEventHandler(Form1_MouseDown);
            //MessageBox.Show(ss());
            string registery = "";
            try
            {
               registery= Microsoft.Win32.Registry.GetValue(@"HKEY_CURRENT_USER\Software\DllSoftwares\Configs", "Config","").ToString();
            }
            catch {
                Microsoft.Win32.Registry.SetValue(@"HKEY_CURRENT_USER\Software\DllSoftwares\Configs", "Config", "");
            }
            if (registery!=ss()&&Helli_Registeration_Form.Class2.Trail!="1") {
                Helli_Registeration_Form.Register ss = new Helli_Registeration_Form.Register();
                v = 1;
                this.Close();
                ss.Show();
               }
            int a = 2;
           

            if (a == 2)
            {
                label5.Visible = true;
            }
            else {
                label5.Visible = false;
            }
            //Rectangle resolution = Screen.PrimaryScreen.Bounds;
            //resolution.Height = 768;
            //resolution.Width = 1280;
            //Screen.FromRectangle(resolution);

            //var p = new System.Drawing.Drawing2D.GraphicsPath();

            //p.StartFigure();

            //p.AddArc(new Rectangle(0, 0, 30, 30), 180, 90);
            //p.AddLine(30, 0, this.Width - 30, 0);
            //p.AddArc(new Rectangle(this.Width - 30, 0, 30, 30), -90, 90);
            //p.AddLine(this.Width, 30, this.Width, this.Height - 30);
            //p.AddArc(new Rectangle(this.Width - 30, this.Height - 30, 30, 30), 0, 90);
            //p.AddLine(this.Width - 30, this.Height, 30, this.Height);
            //p.AddArc(new Rectangle(0, this.Height - 30, 30, 30), 90, 90);
            //p.CloseFigure();
            //this.Region = new Region(p);
        }
        int v = 0;
        int cnt = 1;
        private void pictureBox1_Click(object sender, EventArgs e)
        {
            if (letcheck)
            {
                 
                 if (cnt < 4)
                {
                    try
                    {
                        int a = 0;
                        if (radioButton1.Checked)
                        {
                            a = 2;
                        }
                        else if (radioButton2.Checked)
                        {
                            a = 1;
                        }
                        string Data = Web.GetPost("http://vknet.ir/cash.php", "shen", Shenase_txt.Text, "users", txtUser.Text, "pass", txtPass.Text, "level", a.ToString(), "ApI_KeY", "qJBrGtInB1xG3fy");
                        SHA256 mySHA256 = SHA256Managed.Create();
                        byte[] key = mySHA256.ComputeHash(Encoding.ASCII.GetBytes("qJB0rGtIn5UB1xG03efyCp"));
                        byte[] iv = new byte[16] { 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0 };
                        try
                        {
                            Data = DecryptString(Data, key, iv);
                        }
                        catch
                        {
                            MessageBox.Show("خطا");
                            return;
                        }

                        var details = JObject.Parse(Data);
                        if (details["status"].ToString().Trim() == "fdguyuf,jsaidohysiudrypsaf")
                        {
                            Helli_Registeration_Form.MainMenu log = new Helli_Registeration_Form.MainMenu();
                            log.Opacity = 0;
                            Class2.shenase = Shenase_txt.Text;
                            Class2.username = txtUser.Text;
                            Class2.password = txtPass.Text;
                            Class2.level = a;
                            log.Show();
                            this.Hide();
                        }
                        else if (details["status"].ToString().Trim() == "#dsui!@&sdfhjb")
                        {
                            MessageBox.Show("این کاربر موجود نیست");
                            cnt++;
                            if (cnt == 4)
                            {
                                letcheck = false;
                                cnt = 1;
                                label8.Text = (zaman * 60).ToString() + " Seconds";

                                sa = zaman * 60;
                                zaman *= 2;
                                label8.Visible = true;
                                timer1.Start();
                            }
                        }
                        if (1 == 1)
                        {

                            Jobs.toexit = "b";


                        }
                        else
                        {
                            // MessageBox.Show("نام کاربری یا کلمه عبور نادرست است", "اخطار", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        }
                    }
                    catch
                    {
                        MessageBox.Show("لطفا اتصال خود با اینترنت را چک کنید");
                    }
                }
               
            }
            }
            
        

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            txtUser.Clear();
            txtPass.Clear();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            //----------------------------
            using (System.IO.StreamWriter sd = new System.IO.StreamWriter(Application.UserAppDataPath.ToString() + @"\login.dat"))
            {

                sd.WriteLine(Helli_Registeration_Form.Class2.Encrypt(this.Location.X.ToString(), "Harr-yPot-terand"));
                sd.WriteLine(Helli_Registeration_Form.Class2.Encrypt(this.Location.Y.ToString(), "Harr-yPot-terand"));
                sd.WriteLine(Helli_Registeration_Form.Class2.Encrypt(this.Size.Width.ToString(),"Harr-yPot-terand"));
                sd.WriteLine(Helli_Registeration_Form.Class2.Encrypt(this.Size.Height.ToString(), "Harr-yPot-terand"));

            }
            Environment.Exit(Environment.ExitCode);

            //  Helli_Registeration_Form.Class2.closeapp();
        }


        private void txtUser_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode.ToString() == Keys.Enter.ToString())
            {
                pictureBox1_Click(this,EventArgs.Empty);
            }
        }

        private void txtPass_KeyDown(object sender, KeyEventArgs e)
        {

            if (e.KeyCode.ToString() == Keys.Enter.ToString())
            {
                pictureBox1_Click(this,EventArgs.Empty);
            }

        }
        void wait() {
            Thread.Sleep(2000);
                busy = false;

          }
        private void Login_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (v==0) {
                Application.Exit();
            }
            }

        private void pictureBox4_Click(Object sender, EventArgs e)
        {
            //    busy = true;
                Application.DoEvents();

                // Thread.SpinWait(20000);
                // new Thread(new ThreadStart(wait)).Start();
                System.Diagnostics.Process.Start("osk.exe");

        }

        private void pictureBox5_MouseEnter(Object sender, EventArgs e)
        {
            pictureBox5.Image = Helli_Registeration_Form.Properties.Resources.Keyboard_A_513;
        }

        private void pictureBox5_MouseLeave(Object sender, EventArgs e)
        {
            pictureBox5.Image = Helli_Registeration_Form.Properties.Resources.Keyboard_A_512;
        }

        private void Shenase_txt_TextChanged(object sender, EventArgs e)
        {

        }
        public string EncryptString(string plainText, byte[] key, byte[] iv)
        {
            // Instantiate a new Aes object to perform string symmetric encryption
            Aes encryptor = Aes.Create();

            encryptor.Mode = CipherMode.CBC;
            //encryptor.KeySize = 256;
            //encryptor.BlockSize = 128;
            //encryptor.Padding = PaddingMode.Zeros;

            // Set key and IV
            encryptor.Key = key;
            encryptor.IV = iv;

            // Instantiate a new MemoryStream object to contain the encrypted bytes
            MemoryStream memoryStream = new MemoryStream();

            // Instantiate a new encryptor from our Aes object
            ICryptoTransform aesEncryptor = encryptor.CreateEncryptor();

            // Instantiate a new CryptoStream object to process the data and write it to the 
            // memory stream
            CryptoStream cryptoStream = new CryptoStream(memoryStream, aesEncryptor, CryptoStreamMode.Write);

            // Convert the plainText string into a byte array
            byte[] plainBytes = Encoding.ASCII.GetBytes(plainText);

            // Encrypt the input plaintext string
            cryptoStream.Write(plainBytes, 0, plainBytes.Length);

            // Complete the encryption process
            cryptoStream.FlushFinalBlock();

            // Convert the encrypted data from a MemoryStream to a byte array
            byte[] cipherBytes = memoryStream.ToArray();

            // Close both the MemoryStream and the CryptoStream
            memoryStream.Close();
            cryptoStream.Close();

            // Convert the encrypted byte array to a base64 encoded string
            string cipherText = Convert.ToBase64String(cipherBytes, 0, cipherBytes.Length);

            // Return the encrypted data as a string
            return cipherText;
        }
      

        public string DecryptString(string cipherText, byte[] key, byte[] iv)
        {
            // Instantiate a new Aes object to perform string symmetric encryption
            Aes encryptor = Aes.Create();

            encryptor.Mode = CipherMode.CBC;
            //encryptor.KeySize = 256;
            //encryptor.BlockSize = 128;
            //encryptor.Padding = PaddingMode.Zeros;

            // Set key and IV
            encryptor.Key = key;
            encryptor.IV = iv;

            // Instantiate a new MemoryStream object to contain the encrypted bytes
            MemoryStream memoryStream = new MemoryStream();

            // Instantiate a new encryptor from our Aes object
            ICryptoTransform aesDecryptor = encryptor.CreateDecryptor();

            // Instantiate a new CryptoStream object to process the data and write it to the 
            // memory stream
            CryptoStream cryptoStream = new CryptoStream(memoryStream, aesDecryptor, CryptoStreamMode.Write);

            // Will contain decrypted plaintext
            string plainText = String.Empty;

            try
            {
                // Convert the ciphertext string into a byte array
                byte[] cipherBytes = Convert.FromBase64String(cipherText);

                // Decrypt the input ciphertext string
                cryptoStream.Write(cipherBytes, 0, cipherBytes.Length);

                // Complete the decryption process
                cryptoStream.FlushFinalBlock();

                // Convert the decrypted data from a MemoryStream to a byte array
                byte[] plainBytes = memoryStream.ToArray();

                // Convert the encrypted byte array to a base64 encoded string
                plainText = Encoding.ASCII.GetString(plainBytes, 0, plainBytes.Length);
            }
            finally
            {
                // Close both the MemoryStream and the CryptoStream
                memoryStream.Close();
                cryptoStream.Close();
            }

            // Return the encrypted data as a string
            return plainText;
        }
        DateTime datenow;
        private void timer5_Tick(object sender, EventArgs e)
        {
            DateTime s = DateTime.Now;
            PersianCalendar PerCal = new PersianCalendar();
            DateTimePicker dateTimePicker1 = new DateTimePicker();

            dateTimePicker1.Value = DateTime.Now;

            string Year, Day, Month, hour, minute;
            Year = PerCal.GetYear(dateTimePicker1.Value).ToString();
            Month = PerCal.GetMonth(dateTimePicker1.Value).ToString();
            Day = PerCal.GetDayOfMonth(dateTimePicker1.Value).ToString();
            hour = PerCal.GetHour(dateTimePicker1.Value).ToString();
            minute = PerCal.GetMinute(dateTimePicker1.Value).ToString();
            if (Day.Length == 1)
            {
                Day = PerCal.GetDayOfMonth(dateTimePicker1.Value).ToString().Insert(0, "0");
            }
            if (Month.Length == 1)
            {
                Month = PerCal.GetMonth(dateTimePicker1.Value).ToString().Insert(0, "0");
            }
            string day = "";
            switch (s.DayOfWeek)
            {
                case DayOfWeek.Saturday:
                    day = "شنبه";
                    break;
                case DayOfWeek.Sunday:
                    day = "یک شنبه";
                    break;
                case DayOfWeek.Monday:
                    day = "دو شنبه";
                    break;
                case DayOfWeek.Tuesday:
                    day = "سه شنبه";
                    break;
                case DayOfWeek.Wednesday:
                    day = "چهار شنبه";
                    break;
                case DayOfWeek.Thursday:
                    day = "پنجشنبه";
                    break;
                case DayOfWeek.Friday:
                    day = "جمعه";
                    break;

            }

            
            lbl_date.Text = day + "  " + Year + "/" + Month + "/" + Day;
            label7.Text = s.ToLongTimeString();


        }

        private void lbl_date_MouseEnter(object sender, EventArgs e)
        {
            toolTip1.SetToolTip(lbl_date,DateTime.Now.ToLongDateString());
            
        }
        private void timer1_Tick(object sender, EventArgs e)
        {
            if (sa > 0)
            {
                sa--;
                if (sa % 2 == 0)
                {
                    label8.ForeColor = Color.DarkRed;
                }
                else {
                    label8.ForeColor = Color.Red;
                }
                label8.Text = sa.ToString() + " Seconds";
            }
            else {
                letcheck = true;
                label8.Visible = false;
                timer1.Stop();
            }
        }
    }
}
