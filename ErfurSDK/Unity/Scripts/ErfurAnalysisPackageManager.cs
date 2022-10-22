using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net.Http;
using System.Threading;
using UnityEngine;


namespace ErfurSDK
{
    public static class ErfurAnalysisPackageManager
    {
        private static HttpClient _httpClient = new HttpClient();
        private static string _baseUrl = "";
        private static string _gameId = "";
        private static int _id = 0;
        private static string _token = "";
        private static async void Post(string url, Dictionary<string, string> dictionary)
        {
            var content = new FormUrlEncodedContent(dictionary);
            var response = await _httpClient.PostAsync(url, content);
            //string result = await response.Content.ReadAsStringAsync();

        }
        private static async void GetID()
        {
            if (PlayerPrefs.HasKey("_id") == false)
            {
                var response = await _httpClient.GetStringAsync(_baseUrl + _gameId + "/get_user_id/");
                if (response != "")
                {
                    _id = int.Parse(response);
                    if (_id != 0)
                    {
                        PlayerPrefs.SetInt("_id", _id);
                        _id = PlayerPrefs.GetInt("_id");
                        GetToken();
                    }
                }


            }
            else
            {
                _id = PlayerPrefs.GetInt("_id");
                GetToken();
            }
        }
        private static async void GetToken()
        {
            var response = await _httpClient.GetStringAsync(_baseUrl + _gameId + "/" + _id + "/get_token/");
            if (_id != 0)
            {
                _token = response;
            }
        }
        public static void Initialize(string baseUrl, string gameId)
        {
            _httpClient = new HttpClient();
            Thread.CurrentThread.CurrentCulture = CultureInfo.GetCultureInfo("en-US");
            _baseUrl = baseUrl;
            _gameId = gameId;
            GetID();
        }
        public static void UpdateOrAddValue(string key, string value)
        {

            var dictionary = new Dictionary<string, string>
            {
                { "game_id", _gameId },
                { "id", _id.ToString() },
                { "token", _token },
                { "key", key },
                { "value", value }
            };

            Post(_baseUrl + "game_id", dictionary);
        }
        public static void UpdateOrAddValue(string key, float value)
        {
            UpdateOrAddValue(key, value.ToString());
        }
        public static void UpdateOrAddValue(string key, int value)
        {
            UpdateOrAddValue(key, value.ToString());
        }
        public static void IncreaseOrAddValue(string key, string value)
        {
            
            var dictionary = new Dictionary<string, string>
            {
                { "game_id", _gameId },
                { "id", _id.ToString() },
                { "token", _token },
                { "key", key },
                { "value", value }
            };

            Post(_baseUrl + "game_id_", dictionary);
        } 
        public static void IncreaseOrAddValue(string key, int value)
        {
            IncreaseOrAddValue(key, value.ToString());
        }
        public static void IncreaseOrAddValue(string key, float value)
        {
            var x = Math.Round(value, 3);

            IncreaseOrAddValue(key, x.ToString());
        }
    }
}