using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.IO;
using Wilsonhut.Chunks;

namespace Adventurer3
{
    class Adv3API
    {
        public Adv3API()
        {

        }

        NetworkStream stream;
        public bool connected = false;



        public void Connect(string Ip)
        {
            string server = Ip;
            Int32 port = 8899;
            TcpClient client = new TcpClient(server, port);
            stream = client.GetStream();
            connected = true;
        }


        public string SendGCode(string GCODE)
        {
            string message = "~" + GCODE;
            Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);
            stream.Write(data, 0, data.Length);
            data = new Byte[256];
            String responseData = String.Empty;
            Int32 bytes = stream.Read(data, 0, data.Length);
            responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
            return responseData;
        }

        public void SendTCP(string Data)
        {
            string message = Data;
            Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);
            stream.Write(data, 0, data.Length);
        }


        public void Disconnect()
        {
            connected = false;
            stream.Dispose();
            stream.Close();
        }
    }
}
