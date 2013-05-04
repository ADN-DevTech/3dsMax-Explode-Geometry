#region Copyright
//      .NET Sample
//
//      Copyright (c) 2013 by Autodesk, Inc.
//
//      Permission to use, copy, modify, and distribute this software
//      for any purpose and without fee is hereby granted, provided
//      that the above copyright notice appears in all copies and
//      that both that copyright notice and the limited warranty and
//      restricted rights notice below appear in all supporting
//      documentation.
//
//      AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
//      AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
//      MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.  AUTODESK, INC.
//      DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
//      UNINTERRUPTED OR ERROR FREE.
//
//      Use, duplication, or disclosure by the U.S. Government is subject to
//      restrictions set forth in FAR 52.227-19 (Commercial Computer
//      Software - Restricted Rights) and DFAR 252.227-7013(c)(1)(ii)
//      (Rights in Technical Data and Computer Software), as applicable.
//
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;

namespace NumericEntry
{
    /// <summary>
    /// Interaction logic for NumericEntryControl.xaml
    /// </summary>
    public partial class NumericEntryControl : UserControl
    {
        

        public static readonly DependencyProperty ValueProperty = DependencyProperty.Register("Value",
            typeof(Single), typeof(NumericEntryControl),
            new PropertyMetadata(1.0f));

        public static readonly DependencyProperty MaxValueProperty = DependencyProperty.Register("MaxValue",
            typeof(Single), typeof(NumericEntryControl),
            new PropertyMetadata(100.0f));

        public static readonly DependencyProperty MinValueProperty = DependencyProperty.Register("MinValue",
                    typeof(Single), typeof(NumericEntryControl),
                    new PropertyMetadata(0.1f));

        public static readonly DependencyProperty IncrementProperty = DependencyProperty.Register("Increment", 
            typeof(Single), typeof(NumericEntryControl),
            new PropertyMetadata(0.1f));

        public static readonly DependencyProperty LargeIncrementProperty = DependencyProperty.Register("LargeIncrement",
            typeof(Single), typeof(NumericEntryControl),
            new PropertyMetadata(0.5f));

        private float _previousValue = 0.0f;
        private DispatcherTimer _timer = new DispatcherTimer();
        private static int _delayRate = System.Windows.SystemParameters.KeyboardDelay;
        private static int _repeatSpeed = Math.Max(1, System.Windows.SystemParameters.KeyboardSpeed);
        
        private bool _isIncrementing = false;

        public Single Value
        {
            get
            {
                return (Single)GetValue(ValueProperty);
            }
            set
            {
                SetValue(ValueProperty, value);
            }
        }

        public Single MaxValue
        {
            get
            {
                return (Single)GetValue(MaxValueProperty);
            }
            set
            {
                SetValue(MaxValueProperty, value);
            }
        }

        public Single MinValue
        {
            get
            {
                return (Single)GetValue(MinValueProperty);
            }
            set
            {
                SetValue(MinValueProperty, value);
            }
        }

        public Single Increment
        {
            get
            {
                return (Single)GetValue(IncrementProperty);
            }
            set
            {
                SetValue(IncrementProperty, value);
            }
        }

        public Single LargeIncrement
        {
            get
            {
                return (Single)GetValue(LargeIncrementProperty);
            }
            set
            {
                SetValue(LargeIncrementProperty, value);
            }
        }

        public NumericEntryControl()
        {
            InitializeComponent();

            _textbox.PreviewTextInput += new TextCompositionEventHandler(_textbox_PreviewTextInput);
            _textbox.PreviewKeyDown += new KeyEventHandler(_textbox_PreviewKeyDown);
            _textbox.GotFocus += new RoutedEventHandler(_textbox_GotFocus);
            _textbox.LostFocus += new RoutedEventHandler(_textbox_LostFocus);

            buttonIncrement.PreviewMouseLeftButtonDown += new MouseButtonEventHandler(buttonIncrement_PreviewMouseLeftButtonDown);
            buttonIncrement.PreviewMouseLeftButtonUp += new MouseButtonEventHandler(buttonIncrement_PreviewMouseLeftButtonUp);

            buttonDecrement.PreviewMouseLeftButtonDown += new MouseButtonEventHandler(buttonDecrement_PreviewMouseLeftButtonDown);
            buttonDecrement.PreviewMouseLeftButtonUp += new MouseButtonEventHandler(buttonDecrement_PreviewMouseLeftButtonUp);

            _timer.Tick += new EventHandler(_timer_Tick);
        }

        void buttonIncrement_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            buttonIncrement.CaptureMouse();
            _timer.Interval = TimeSpan.FromMilliseconds(_delayRate * 250);
            _timer.Start();

            _isIncrementing = true;
        }

        void buttonIncrement_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            _timer.Stop();
            buttonIncrement.ReleaseMouseCapture();
            IncrementValue();
        }

        void buttonDecrement_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            buttonDecrement.CaptureMouse();
            _timer.Interval = TimeSpan.FromMilliseconds(_delayRate * 250);
            _timer.Start();

            _isIncrementing = false;
        }

        void buttonDecrement_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            _timer.Stop();
            buttonDecrement.ReleaseMouseCapture();
            DecrementValue();
        }

        void _timer_Tick(object sender, EventArgs e)
        {
            if (_isIncrementing)
            {
                IncrementValue();
            }
            else
            {
                DecrementValue();
            }
            _timer.Interval = TimeSpan.FromMilliseconds(1000.0 / _repeatSpeed);
            
        }

        void _textbox_GotFocus(object sender, RoutedEventArgs e)
        {
            _previousValue = Value;
        }

        void _textbox_LostFocus(object sender, RoutedEventArgs e)
        {
            float newValue = 0;
            if (Single.TryParse(_textbox.Text, out newValue))
            {
                if (newValue > MaxValue)
                {
                    newValue = MaxValue;
                }
                else if (newValue < MinValue)
                {
                    newValue = MinValue;
                }                
            }
            else
            {
                newValue = _previousValue;
            }
            _textbox.Text = newValue.ToString();
        }

        void _textbox_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            if (!IsNumericInput(e.Text))
            {
                e.Handled = true;
                return;
            }
        }
       
        private bool IsNumericInput(string text)
        {
            foreach (char c in text)
            {
                if ((!char.IsDigit(c)) && !c.Equals('.'))
                {
                    return false;
                }
            }
            return true;
        }

        void _textbox_PreviewKeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                case Key.Up:
                    IncrementValue();
                    break;
                case Key.Down:
                    DecrementValue();
                    break;
                case Key.PageUp:
                    Value = Math.Min(Value + LargeIncrement, MaxValue);
                    break;
                case Key.PageDown:
                    Value = Math.Max(Value - LargeIncrement, MinValue);
                    break;
                default:
                    //do nothing
                    break;
            }
        }

        private void IncrementValue()
        {
            Value = Math.Min(Value + Increment, MaxValue);
        }

        private void DecrementValue()
        {
            Value = Math.Max(Value - Increment, MinValue);
        }

        
    }
}
