import React from 'react';

function Step1({ nextStep }) {
  return (
    <div className="step-form">
      <h1>AHEAD OF YOUR SHOW</h1>
      <p>We’ve summarised the main points to know below but you can read the full ‘How To Do A Show on RBV’ docs here:</p>
      <ul>
        <li><a href="link_to_doing_live_show_pdf">Doing a Live Show on RBV</a></li>
        <li><a href="link_to_doing_pre_recorded_show_pdf">Doing a Pre-Recorded Show on RBV</a></li>
      </ul>

      <h2>ADVANCE SOCIAL MEDIA PROMO</h2>
      <p>What we do:</p>
      <ul>
        <li>Tuesday of the week of your show – we post the daily schedules for Wednesday to Sunday and tag you in them so you can share on your own socials.</li>
        <li>The day of your show – we post your individual show posts with your image/show name/ genres etc and again tag you so you can share.</li>
      </ul>

      <p>What we ask from you:</p>
      <ul>
        <li>Read through the info below</li>
        <li>Submit all the required info on the following page (* Please note, if you miss the deadline to upload your info/ image/mp3 file unfortunately it will not be included when the socials and schedule go out/your show will not be aired.)</li>
      </ul>

      <h2>FILES & FORMATTING</h2>
      <ul>
        <li>We recommend you put your music files through Rekordbox and double-check your USB is formatted as suggested in our info doc before arriving with your music files in mp3 or wav format only.</li>
      </ul>

      <h2>ON THE DAY</h2>
      <ul>
        <li>Please turn up at least 15 mins before the start of your show.</li>
        <li>You'll get access to set up in the radio booth/check your USB 5 mins before your show starts, and help the next host 5 mins before the end of your show.</li>
        <li>Follow the instructions of the volunteer radio producer for any technical help.</li>
        <li>You get a 10% discount at Café Buena Vida on the day of your show.</li>
        <li>Please do not place any drinks/food on the decks or electrical equipment.</li>
      </ul>

      <button className="btn" onClick={nextStep}>Next</button>
      </div>
  );
}

export default Step1;
