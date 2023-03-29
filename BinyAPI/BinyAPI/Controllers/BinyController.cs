using Microsoft.AspNetCore.Mvc;
using System.Xml;
using HtmlAgilityPack;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium;
using System;

namespace BinyAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class BinyController : ControllerBase
    {
        [HttpGet(Name = "GetBin")]
        public string GetBin(string UPRN)
        {
            //906700527049
            var url = "https://www.glasgow.gov.uk/forms/refuseandrecyclingcalendar/CollectionsCalendar.aspx?UPRN=" + UPRN;
            return GetNextBins(url);

        }

        private string GetNextBins(string url)
        {
            var web = new HtmlWeb();
            var doc = web.Load(url);

            var coloredBins = GetImgs(doc, false);
            if (coloredBins != "")
            {
                return coloredBins;
            }

            var options = new ChromeOptions();
            options.AddArgument("--headless");
            using (var driver = new ChromeDriver(options))
            {
                driver.Navigate().GoToUrl(url);

                var nextMonthLink = driver.FindElement(By.XPath("//a[@title='Go to the next month']"));
                nextMonthLink.Click();

                Thread.Sleep(20000);

                var newHtml = driver.PageSource;
                doc = new HtmlDocument();
                doc.LoadHtml(newHtml);

                return GetImgs(doc, true);

            }
        }

        private string GetImgs(HtmlDocument doc, bool isNextMonth)
        {
            List<string> words = new List<string> { "greenBin", "blueBin", "brownBin", "purpleBin" }; // list of words to check
            var calendarTable = doc.DocumentNode.SelectSingleNode("//table[@id='Application_Calendar']");
            if (calendarTable == null)
            {
                throw new Exception("Could not find table with id 'Application_Calendar'");
            }

            var todayTd = calendarTable.Descendants("td")
                .FirstOrDefault(td => (td.GetAttributeValue("title", "").Contains("today")) 
                || (td.GetAttributeValue("class", "").Contains("CalendarTodayDayStyle CalendarDayStyle") && isNextMonth));
           
            while (todayTd != null)
            {
                var imgs = todayTd.Descendants("img");                

                if (imgs.Count() > 0)
                {
                    string nextBin = string.Join(",", imgs.SelectMany(img => words.Where(word => img.GetAttributeValue("src", "").Contains(word))));
                    return nextBin;
                }

                todayTd = todayTd.NextSibling;
                //while (todayTd != null && todayTd.NodeType != HtmlNodeType.Element)
                //{
                //    todayTd = todayTd.NextSibling;
                //}
            }

            return "";
        }



    }


}
