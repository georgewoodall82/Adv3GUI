using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.IO;

namespace Adventurer3
{
    public partial class Form1 : Form
    {
        Adv3API api = new Adv3API();
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OutputLabel.Text = "Output: " + api.SendGCode(textBox1.Text);
        }

        private void Second()
        {
            if (api.connected == true)
            {
                TemperatureLabel.Text = api.SendGCode("M105").Replace("CMD M105 Received.", "").Replace("ok", "").Replace("T0:", "Extruder: ").Replace(" /", "/").Replace("B:", "Bed: ");
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            Second();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            api.Connect(textBox2.Text);
            timer1.Enabled = true;
            button3.Enabled = api.connected;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            api.Disconnect();
            button3.Enabled = api.connected;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "GCode (*.g, *.gcode, *.gx)|*.g;*.gcode;*.gx|All Files (*.*)|*.*";
            DialogResult result = openFileDialog1.ShowDialog();
            if (result == DialogResult.OK)
            {
                StreamReader sr = new StreamReader(openFileDialog1.FileName);
                string sendgc = sr.ReadToEnd();
                sr.Close();
                api.SendGCode("M28 780275 0:/user/testapi.gx");
                System.Threading.Thread.Sleep(1000);
                api.SendTCP(sendgc);
                System.Threading.Thread.Sleep(1000);
                api.SendGCode("M29");
                System.Threading.Thread.Sleep(1000);
                api.SendGCode("M23 0:/user/testapi.gx");
            }
        }
    }
}
